# Changelog

All notable changes to this project will be documented in this file.

## 0.1.1 - 2026-10-18

- Treat pull-request content as untrusted data rather than agent instructions.
- Require an isolated, credential-free, network-disabled environment before
  executing contributor-controlled tests or builds.
- Add repository validation for the security boundary requirements.

## 0.1.0 - 2026-10-18

- Initial public release.
- Review pull requests using their base/head revisions and complete diff.
- Prioritize correctness, regression, security, and testing risks with
  file-level evidence.
- Keep reviews read-only unless the user separately requests changes.
