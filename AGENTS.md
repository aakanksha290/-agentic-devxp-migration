# AGENTS.md

Instructions for any coding agent (Codex, Copilot agent, Claude, etc.).
Single source of truth: see `.github/copilot-instructions.md`.

Hard rules (repeat here because they matter most):
- Never commit secrets.
- Never merge, deploy or approve. Open a PR and let a human review it.
- Pipelines must call `.github/workflows/reusable-*.yml`.
