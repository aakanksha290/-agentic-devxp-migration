---
mode: agent
description: Migrate one Jenkinsfile to a GitHub Actions workflow using our reusable workflows
---
You are helping migrate a legacy Jenkins pipeline to GitHub Actions.

Input: the Jenkinsfile at ${input:jenkinsfile:path to Jenkinsfile}

Steps:
1. Read the Jenkinsfile and list every stage, credential, plugin and trigger in a table.
2. Map each item using `.github/instructions/workflows.instructions.md`.
3. Write the new workflow to `.github/workflows/<service-name>.yml`.
   It MUST call the reusable workflows instead of copying steps.
4. Run `python scripts/validate_workflows.py .github/workflows` and fix any errors.
5. In your answer, list:
   - anything you could NOT map (with `# TODO(migration)` in the file)
   - any assumption you made
   - which secrets/environments a human must create in GitHub settings

Do not invent actions or inputs. Do not remove functionality silently.
A human will review and test this before merge.
