#!/usr/bin/env python3
"""Generate a repository preview from the recorded acceptance run."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[1]
LOGO = REPO_ROOT / "plugins" / "github-pr-helper" / "assets" / "logo.png"
OUTPUT = REPO_ROOT / "docs" / "images" / "usage-preview.png"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for candidate in (
        Path("C:/Windows/Fonts") / name,
        Path("/usr/share/fonts/truetype/dejavu") / name,
    ):
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def main() -> None:
    image = Image.new("RGB", (1200, 630), "#0d1117")
    draw = ImageDraw.Draw(image)

    for x in range(0, 1200, 32):
        for y in range(0, 630, 32):
            draw.ellipse((x, y, x + 2, y + 2), fill="#161b22")

    draw.rounded_rectangle((68, 52, 1132, 578), radius=30, fill="#161b22", outline="#30363d", width=2)
    logo = Image.open(LOGO).convert("RGBA").resize((112, 112), Image.Resampling.LANCZOS)
    image.paste(logo, (104, 92), logo)

    draw.text((244, 94), "GitHub PR Helper", fill="#f0f6fc", font=font("segoeuib.ttf", 46))
    draw.text(
        (246, 154),
        "Evidence-backed review with real base/head and full diff",
        fill="#8b949e",
        font=font("segoeui.ttf", 23),
    )

    draw.rounded_rectangle((246, 196, 468, 236), radius=20, fill="#1f6feb")
    draw.text((269, 204), "ACCEPTANCE RUN", fill="#ffffff", font=font("segoeuib.ttf", 16))
    draw.text((486, 202), "2026-10-18  ·  PR #3199", fill="#8b949e", font=font("segoeui.ttf", 18))

    draw.rounded_rectangle((104, 256, 1096, 348), radius=18, fill="#0d1117", outline="#30363d", width=2)
    draw.text((132, 276), "$", fill="#3fb950", font=font("consola.ttf", 25))
    draw.text(
        (170, 276),
        "github-pr-review review: https://github.com/openai/openai-cookbook/pull/3199",
        fill="#f0f6fc",
        font=font("consola.ttf", 21),
    )
    draw.text((132, 312), "read-only  ·  base/head verified  ·  complete diff", fill="#8b949e", font=font("consola.ttf", 19))

    cards = [
        ("SCOPE", "2 files", "20 additions · 8 deletions"),
        ("FINDINGS", "2 × P2", "path-specific and reproducible"),
        ("VALIDATION", "70 passed", "1 skipped · 22 environment failures"),
    ]
    left = 104
    for title, value, detail in cards:
        draw.rounded_rectangle((left, 378, left + 310, 514), radius=18, fill="#0d1117", outline="#30363d", width=2)
        draw.text((left + 24, 397), title, fill="#58a6ff", font=font("segoeuib.ttf", 15))
        draw.text((left + 24, 430), value, fill="#f0f6fc", font=font("segoeuib.ttf", 34))
        draw.text((left + 24, 478), detail, fill="#8b949e", font=font("segoeui.ttf", 16))
        left += 338

    draw.text((104, 536), "P0–P3 findings  ·  repository-relative paths  ·  tests separated from inference", fill="#8b949e", font=font("segoeui.ttf", 18))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
