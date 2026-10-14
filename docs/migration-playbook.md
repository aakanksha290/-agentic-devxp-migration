# Jenkins -> GitHub Actions migration playbook

## The 5 phases
| # | Phase | What happens | Tooling |
|---|---|---|---|
| 1 | **Audit** | Inventory every Jenkins job: stages, plugins, credentials, agents | `scripts/jenkins_inventory.py`, `gh actions-importer audit jenkins` |
| 2 | **Standardise** | Group pipelines into patterns; build one reusable workflow per pattern | `.github/workflows/reusable-*.yml` |
| 3 | **Convert** | Generate the new workflow (Actions Importer, or AI with our prompt file) | `gh actions-importer dry-run`, `.github/prompts/migrate-jenkinsfile.prompt.md` |
| 4 | **Validate** | Guardrail checks + run old and new pipelines **side by side** and compare | `guardrails.yml`, actionlint, PR review |
| 5 | **Cut over** | Switch team by team, freeze the Jenkins job, then decommission | Branch protection required checks |

Start with a **pilot team** (simple, friendly service), learn, then scale in waves.

## Concept mapping
| Jenkins | GitHub Actions |
|---|---|
| Jenkinsfile | `.github/workflows/*.yml` |
| `stage` / `steps` | `jobs` / `steps` |
| `agent { label }` | `runs-on: ubuntu-latest` or self-hosted runner labels |
| Shared Library | Reusable workflow (`workflow_call`) or composite action |
| `withCredentials` | `secrets.*`, better: **OIDC** to cloud (no stored keys) |
| `parallel` | `strategy.matrix` / separate jobs |
| `post { always / failure }` | `if: always()` / `if: failure()` |
| `input` (manual approval) | **Environment** with required reviewers |
| `when { branch 'main' }` | `if: github.ref == 'refs/heads/main'` |
| `BUILD_NUMBER` | `github.run_number` / `github.sha` |
| Plugins | Marketplace actions (pinned to tag or SHA) |
| Jenkins agents / VMs | GitHub-hosted runners or self-hosted (e.g. Actions Runner Controller on Kubernetes) |

## Before -> after in this repo
- Before: `legacy-jenkins/payments-service/Jenkinsfile` (~75 lines, password-based registry login, Jenkins `input`)
- After: `.github/workflows/payments-service.yml` (calls 3 reusable workflows, GITHUB_TOKEN for registry, environment approval)

## GitHub Actions Importer commands
```bash
gh extension install github/gh-actions-importer
gh actions-importer audit jenkins --output-dir audit/          # what can be converted?
gh actions-importer dry-run jenkins --source-url <job-url> --output-dir out/
gh actions-importer migrate jenkins --source-url <job-url> --target-url <repo-url> --output-dir out/   # opens a PR
```

## Where AI fits in the migration
- **Explain** complex Jenkinsfiles / shared library Groovy before converting
- **Convert** what the Importer can't (custom Groovy, unusual plugins) using the prompt file
- **Review** the generated PR (opt-in `ai-review` label)
- Always followed by guardrails + side-by-side run + human approval

## Metrics to show progress
- % pipelines migrated, % using reusable workflows
- DORA: deployment frequency, lead time for changes, change failure rate, time to restore
- Pipeline duration & failure rate before vs after
