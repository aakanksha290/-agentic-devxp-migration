# Platform adoption plan

Adoption is earned, not forced. Make the standard path the **easiest** path.

1. **Golden path templates** - starter workflows (`workflow-templates/`) give a working pipeline in one click.
2. **Pilot team first** - migrate one friendly team, fix their pain points, publish their success story.
3. **Champions** - one person per team who knows the platform and gives feedback.
4. **Docs with examples** - before/after examples beat long policy documents.
5. **Office hours + feedback loop** - fortnightly session; track requests as GitHub issues.
6. **Measure** - % migrated, pipeline time, failure rate, DORA metrics; share a dashboard.
7. **Flexibility with guardrails** - teams can add steps, but the non-negotiables
   (permissions, secret handling, prod approval, required checks) are enforced by rulesets.

## Balancing standardisation vs real-world constraints
- Standardise the **what** (security, approvals, reporting), allow choice in the **how**.
- Reusable workflows take inputs, so teams customise without forking.
- Exceptions are allowed but documented and time-boxed.
