# Agentic DevXP Platform - Jenkins to GitHub Actions migration

A working reference project showing how to **modernise CI/CD** (Jenkins -> GitHub Actions)
and make the developer platform **AI-ready, with safe guardrails**.

> Practical AI for real engineering problems: migration, code understanding,
> testing and review, always with validation layers and a human in the loop.

## What's inside (mapped to the role)

| JD area | Where in this repo |
|---|---|
| Migrate legacy Jenkins pipelines | `legacy-jenkins/` (before) -> `.github/workflows/payments-service.yml` (after) |
| Reusable workflows, templates, standards | `.github/workflows/reusable-*.yml`, `.github/actions/setup-python-app/`, `workflow-templates/` |
| Developer tooling (Python) | `scripts/jenkins_inventory.py` (audit), `scripts/validate_workflows.py` (policy check) |
| Containers, Kubernetes | `app/Dockerfile`, `k8s/deployment.yaml`, `reusable-k8s-deploy.yml` |
| PRs, CODEOWNERS, repo standards | `.github/CODEOWNERS`, `.github/pull_request_template.md`, `docs/agent-ready-repo-standard.md` |
| Observability | Job summary in `payments-service.yml`, metrics in `docs/migration-playbook.md` |
| Repository-level AI context | `.github/copilot-instructions.md`, `.github/instructions/`, `.github/prompts/`, `CLAUDE.md`, `AGENTS.md` |
| AI-assisted migration | `.github/prompts/migrate-jenkinsfile.prompt.md` |
| Guardrails / validation layer | `.github/workflows/guardrails.yml` (Jira link, actionlint, policy, secret scan) |
| Human-in-the-loop AI | `.github/workflows/ai-review.yml` (opt-in, comment-only, CODEOWNER still approves) |
| AI risks | `docs/ai-guardrails.md`, `examples/bad-ai-output/` |
| Adoption / golden paths | `docs/adoption-golden-path.md`, `workflow-templates/` |

## Folder layout
```
agentic-devxp-migration/
├── legacy-jenkins/              # BEFORE: two fragmented Jenkinsfiles
├── app/                         # sample Flask service + tests + Dockerfile
├── k8s/                         # Kubernetes deployment + service
├── .github/
│   ├── workflows/
│   │   ├── reusable-python-ci.yml      # golden path: test + lint
│   │   ├── reusable-docker-build.yml   # golden path: image build/push (no stored passwords)
│   │   ├── reusable-k8s-deploy.yml     # golden path: deploy with environment approval + rollback
│   │   ├── payments-service.yml        # AFTER: migrated pipeline, ~50 lines calling the above
│   │   ├── guardrails.yml              # required checks on every PR
│   │   └── ai-review.yml               # opt-in AI reviewer (comments only)
│   ├── actions/setup-python-app/       # composite action
│   ├── instructions/                   # path-specific AI rules (applyTo)
│   ├── prompts/                        # reusable prompt: migrate a Jenkinsfile
│   ├── copilot-instructions.md         # repo-wide AI rules (single source of truth)
│   ├── CODEOWNERS
│   └── pull_request_template.md
├── CLAUDE.md / AGENTS.md        # point other agents at the same rules
├── scripts/                     # Python tooling (audit + policy validation)
├── workflow-templates/          # starter workflow for the org .github repo
├── examples/bad-ai-output/      # what unsafe AI output looks like (validator catches it)
└── docs/                        # playbook, guardrails, repo standard, adoption plan
```

## Run the demo locally
```bash
pip install -r app/requirements.txt

# 1. AUDIT - what do our Jenkins pipelines use?
python scripts/jenkins_inventory.py legacy-jenkins

# 2. VALIDATE - do our workflows follow platform rules?
python scripts/validate_workflows.py .github/workflows            # all PASS

# 3. GUARDRAIL DEMO - unsafe "AI-generated" workflow gets caught
python scripts/validate_workflows.py examples/bad-ai-output       # 6 problems found

# 4. App tests
cd app && pytest -q
```

## The migration flow (end to end)
1. **Audit** Jenkins jobs (`jenkins_inventory.py` / `gh actions-importer audit`) and group them by pattern.
2. **Build reusable workflows** for each pattern (platform team owns them via CODEOWNERS).
3. **Convert** each pipeline with Actions Importer or AI (prompt file + instruction files give the AI context).
4. **Validate**: guardrails run automatically -> AI review (optional) -> CODEOWNER approves -> run side by side with Jenkins.
5. **Cut over** team by team; prod deploys always need environment approval.

## Human-in-the-loop
```
AI drafts -> automated checks -> PR -> CODEOWNERS review -> merge -> deploy (human-approved environment)
```
AI can suggest and comment. It cannot approve, merge or deploy.

## To run it for real on GitHub
1. Push this folder as its own repository.
2. Settings > Environments > create `production` with required reviewers.
3. Settings > Rules > require PRs, CODEOWNERS review, and the `guardrails` checks.
4. Add secrets `KUBECONFIG_B64` (or switch to OIDC) and `ANTHROPIC_API_KEY` (for ai-review).
5. Add repo variable `DEPLOY_ENABLED=true` to switch on the production deploy job.
