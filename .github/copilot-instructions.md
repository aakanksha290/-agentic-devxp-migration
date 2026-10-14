# Repository instructions for AI assistants (GitHub Copilot / Claude / other agents)

This repo is the payments-service plus the shared CI/CD platform workflows.

## Project facts
- App code: `app/` (Python 3.12, Flask). Tests: `pytest` in `app/`. Lint: `flake8 --max-line-length=120`.
- Container: `app/Dockerfile` -> pushed to `ghcr.io`.
- Deploy: Kubernetes manifests in `k8s/`.
- Legacy Jenkins pipelines (read-only reference): `legacy-jenkins/`.

## Rules for CI/CD changes
- New pipelines MUST call the reusable workflows in `.github/workflows/reusable-*.yml`.
  Do not copy their steps inline.
- Every workflow MUST have a top-level `permissions:` block with least privilege.
- Never use `@main` or `@master` for actions. Use a version tag or commit SHA.
- Never put secrets, tokens, passwords or internal hostnames in code or YAML.
  Use `${{ secrets.NAME }}` and prefer OIDC for cloud logins.
- Never interpolate `${{ github.event.* }}` directly inside `run:`; pass it through `env:`.
- Production deploys MUST go through the `production` environment (human approval).

## How to behave
- If you are not sure an action, input or flag exists, SAY SO. Do not invent it.
- Keep changes small and explain what you changed in the PR description.
- Run `python scripts/validate_workflows.py .github/workflows` before proposing workflow changes.
