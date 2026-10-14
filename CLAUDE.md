# CLAUDE.md

Claude Code reads this file automatically. The full rules live in
`.github/copilot-instructions.md` so all AI tools share ONE source of truth.

@.github/copilot-instructions.md

## Useful commands
- Run tests: `cd app && pytest -q`
- Validate workflows: `python scripts/validate_workflows.py .github/workflows`
- Inventory Jenkins pipelines: `python scripts/jenkins_inventory.py legacy-jenkins`
