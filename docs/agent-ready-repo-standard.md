# Agent-ready repository standard

Every repository on the platform should have these files. A repo that has them is
easier for both new engineers and AI agents to work in.

| File | Purpose | Owner |
|---|---|---|
| `README.md` | What the service is, how to run & test it | Team |
| `.github/CODEOWNERS` | Mandatory reviewers per path | Team + platform |
| `.github/pull_request_template.md` | Jira link, AI-usage disclosure, test evidence | Platform (standard) |
| `.github/copilot-instructions.md` | Repo-wide rules for AI tools | Team + platform/security |
| `.github/instructions/*.instructions.md` | Path-specific rules (`applyTo:`) | Team |
| `.github/prompts/*.prompt.md` | Reusable prompts for common tasks (e.g. migration) | Platform |
| `CLAUDE.md` / `AGENTS.md` | Pointers for Claude / other agents (link to the single source of truth) | Team |
| `.github/workflows/*.yml` | Must call platform reusable workflows | Team |

## What goes INTO instruction files
- Build / test / lint commands
- Folder structure and conventions
- "Never do" rules (secrets, `@main`, skipping approvals)
- "Say when unsure" instruction

## What NEVER goes in
- Secrets, tokens, internal hostnames, customer data

## Repo settings (enforced with org rulesets)
- Require PR, 1+ approvals, CODEOWNERS review
- Required status checks: `guardrails`, CI
- No force push to `main`
