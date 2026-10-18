#!/usr/bin/env python3
"""Validate the plugin repository without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


PLUGIN_NAME = "github-pr-helper"
MARKETPLACE_NAME = "github-pr-helper-plugins"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")


def require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        fail(f"{label} must be {expected!r}, got {actual!r}")


def validate_skill(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        fail(f"missing SKILL.md in {skill_dir}")

    text = skill_file.read_text(encoding="utf-8")
    if "[TODO:" in text:
        fail(f"unfinished placeholder in {skill_file}")
    if not text.startswith("---\n"):
        fail(f"missing YAML frontmatter in {skill_file}")

    try:
        frontmatter = text.split("---", 2)[1]
    except IndexError:
        fail(f"unterminated YAML frontmatter in {skill_file}")

    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')

    require_equal(fields.get("name"), skill_dir.name, f"{skill_file} skill name")
    if not fields.get("description"):
        fail(f"missing description in {skill_file}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    plugin_root = repo_root / "plugins" / PLUGIN_NAME
    marketplace_file = repo_root / ".agents" / "plugins" / "marketplace.json"
    portable_file = plugin_root / "plugin.json"
    codex_file = plugin_root / ".codex-plugin" / "plugin.json"

    marketplace = load_json(marketplace_file)
    require_equal(marketplace.get("name"), MARKETPLACE_NAME, "marketplace name")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        fail("marketplace must contain exactly one plugin entry")

    entry = entries[0]
    require_equal(entry.get("name"), PLUGIN_NAME, "marketplace plugin name")
    require_equal(entry.get("source", {}).get("path"), f"./plugins/{PLUGIN_NAME}", "source path")
    require_equal(entry.get("policy", {}).get("installation"), "AVAILABLE", "installation policy")
    if entry.get("policy", {}).get("authentication") not in {"ON_INSTALL", "ON_USE"}:
        fail("invalid authentication policy")

    portable = load_json(portable_file)
    codex_manifest = load_json(codex_file)
    for manifest, label in ((portable, "portable manifest"), (codex_manifest, "Codex manifest")):
        require_equal(manifest.get("name"), PLUGIN_NAME, f"{label} name")
        if not SEMVER.match(str(manifest.get("version", ""))):
            fail(f"{label} version is not strict semver")
        if not manifest.get("description"):
            fail(f"{label} is missing a description")
        if not manifest.get("author", {}).get("name"):
            fail(f"{label} is missing author.name")

    require_equal(codex_manifest.get("skills"), "./skills/", "Codex skills path")
    skill_root = plugin_root / "skills"
    skill_dirs = sorted(path for path in skill_root.iterdir() if path.is_dir())
    if not skill_dirs:
        fail("plugin must contain at least one skill")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir)

    print(f"validated {PLUGIN_NAME}@{MARKETPLACE_NAME}")
    print(f"skills: {', '.join(path.name for path in skill_dirs)}")


if __name__ == "__main__":
    try:
        main()
    except OSError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
