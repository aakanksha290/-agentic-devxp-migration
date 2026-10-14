# GUARDRAIL: checks every GitHub Actions workflow against our platform rules.
# Runs in CI (guardrails.yml) on every PR - whether a human or an AI wrote the YAML.
# This is how we catch AI hallucinations and unsafe patterns automatically.
#
# Usage: python scripts/validate_workflows.py .github/workflows

import os
import re
import sys

import yaml


def check_workflow(path):
    errors = []

    with open(path, encoding="utf-8") as f:
        text = f.read()

    # Rule 1: file must be valid YAML
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return [f"invalid YAML: {e}"]

    # Rule 2: must declare permissions (least privilege)
    if "permissions" not in data:
        errors.append("missing top-level 'permissions:' block")

    # Rule 3: no actions pinned to a moving branch
    for action in re.findall(r"uses:\s*([^\s#]+)", text):
        if action.startswith("./"):
            continue  # local action / reusable workflow - fine
        if "@" not in action:
            errors.append(f"action has no version: {action}")
        elif action.endswith("@main") or action.endswith("@master"):
            errors.append(f"action pinned to a branch (use tag or SHA): {action}")

    # Rule 4: no hardcoded secrets
    secret_pattern = r"(password|passwd|token|api_key)\s*[:=]\s*['\"]?[A-Za-z0-9]{8,}"
    if re.search(secret_pattern, text, re.IGNORECASE):
        errors.append("looks like a hardcoded secret")

    # Rule 5: no script injection - github.event values used directly inside run:
    for line in text.splitlines():
        if "run:" in line and "${{ github.event." in line:
            errors.append("github.event value used directly in 'run:' (pass it via env:)")

    # Rule 6: every normal job needs a timeout (jobs that call reusable workflows are skipped)
    jobs = data.get("jobs", {}) or {}
    for job_name, job in jobs.items():
        if "uses" in job:
            continue
        if "steps" in job and "timeout-minutes" not in job:
            errors.append(f"job '{job_name}' has no timeout-minutes")

    return errors


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else ".github/workflows"
    total_errors = 0

    for name in sorted(os.listdir(folder)):
        if not name.endswith((".yml", ".yaml")):
            continue
        path = os.path.join(folder, name)
        errors = check_workflow(path)
        if errors:
            print(f"FAIL  {name}")
            for e in errors:
                print(f"      - {e}")
            total_errors += len(errors)
        else:
            print(f"PASS  {name}")

    print()
    if total_errors:
        print(f"{total_errors} problem(s) found")
        sys.exit(1)
    print("All workflows follow the platform rules")


if __name__ == "__main__":
    main()
