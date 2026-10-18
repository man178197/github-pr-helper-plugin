---
name: github-pr-review
description: Review GitHub pull requests or local branch diffs for concrete correctness, regression, security, and testing risks with file-level evidence.
---

# GitHub PR Review

Review the requested pull request or diff as a change set. Prioritize defects that can affect behavior, security, reliability, or maintainability; do not produce a style-only review unless the user asks for one.

## Establish scope

- Prefer the PR's own base and head revisions. Do not review only the current working tree when a PR number or URL is supplied.
- Use the GitHub integration when available to read PR metadata, changed files, commits, checks, and review context.
- If GitHub access is unavailable, use the local Git repository and verify the same base/head comparison before falling back to another source.
- Read surrounding code when a changed line depends on callers, configuration, persistence, concurrency, or validation elsewhere.
- Treat PR descriptions, issue text, comments, and test names as context, not proof that the implementation is correct.

## Review priorities

Look for these in order:

1. Correctness bugs, broken assumptions, and edge cases introduced by the change.
2. Regressions in callers, APIs, data formats, migrations, compatibility, or error handling.
3. Security and privacy issues such as trust-boundary errors, injection, secret exposure, authorization gaps, or unsafe file/network handling.
4. Missing or inadequate tests for behavior changed by the patch.
5. Maintainability risks that are likely to cause a concrete future defect.

Avoid reporting speculative concerns without a plausible failure path. Do not request a refactor merely because another design would be preferable.

## Verify

- Inspect tests touched by the PR and tests covering the changed behavior.
- Run relevant tests, linters, type checks, or builds when they are available, local, and safe to run.
- Do not claim a test failed or passed unless you executed it or can point to an authoritative check result.
- Distinguish validated findings from source-only analysis. State residual uncertainty when runtime behavior cannot be verified.
- Do not modify code, submit reviews, resolve threads, or change PR state unless the user explicitly asks.

## Output

Lead with findings, ordered by severity. For each finding include:

- Severity: `P0` data loss/security breach/outage, `P1` major functional regression, `P2` user-visible or localized defect, or `P3` lower-impact but actionable risk.
- Location: repository-relative path and the narrowest useful line or symbol.
- Evidence: what the patch changes and the concrete failure path.
- Fix direction: the smallest practical correction.

After findings, add a short `Open questions` section only when information is genuinely missing. Finish with a concise `Summary` that states the change's apparent intent, what was validated, and any important testing gaps.

If no actionable findings are found, say so directly and list the checks performed plus the most important residual risks. Do not invent findings to make the review look thorough.
