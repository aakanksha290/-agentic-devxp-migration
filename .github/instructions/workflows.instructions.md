---
applyTo: ".github/workflows/**/*.yml"
---
# Extra rules that apply ONLY when editing GitHub Actions workflow files

- Jenkins -> GitHub Actions mapping to follow:
  - `stage`/`steps` -> `jobs`/`steps`
  - `agent { label }` -> `runs-on`
  - `parallel` -> `strategy.matrix` or separate jobs
  - `post { always }` -> `if: always()`; `post { failure }` -> `if: failure()`
  - `input` -> `environment:` with required reviewers
  - `withCredentials` -> `secrets` (or OIDC)
  - Shared Library call -> reusable workflow (`uses: ./.github/workflows/reusable-*.yml`)
- Add `timeout-minutes` to every job.
- Use `concurrency` for deploy jobs.
- If a Jenkins plugin has no clear equivalent, add a `# TODO(migration): ...` comment
  instead of guessing.
