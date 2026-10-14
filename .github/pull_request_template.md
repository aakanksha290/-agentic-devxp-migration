## Jira ticket
<!-- e.g. PAY-123 (also put it in the PR title) -->

## What changed and why

## AI assistance
- [ ] No AI used
- [ ] AI-assisted (tool: ______ ) - I have **read and understood every line** it produced
- [ ] AI-generated migration - I compared it against the original Jenkinsfile (see checklist below)

## Migration checklist (only for Jenkins -> GitHub Actions PRs)
- [ ] Every Jenkins stage has a matching job/step
- [ ] Credentials moved to GitHub secrets / OIDC (nothing hardcoded)
- [ ] `permissions:` block is present and minimal
- [ ] Manual approvals use a GitHub **environment**, not a workaround
- [ ] Ran old and new pipeline side by side and outputs match (link both runs)

## Testing
<!-- how did you verify this? -->
