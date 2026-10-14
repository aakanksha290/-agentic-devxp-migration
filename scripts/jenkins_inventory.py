# STEP 1 OF MIGRATION: AUDIT
# Scans a folder for Jenkinsfiles and reports what each pipeline uses,
# so we can group similar pipelines and decide which reusable workflow fits.
#
# Usage: python scripts/jenkins_inventory.py legacy-jenkins

import os
import re
import sys

# Things in a Jenkinsfile that need special attention during migration
RISKY_ITEMS = {
    "withCredentials": "credentials -> move to GitHub secrets / OIDC",
    "input": "manual approval -> GitHub environment",
    "@Library": "shared library -> reusable workflow",
    "parallel": "parallel -> matrix or separate jobs",
    "slackSend": "plugin -> Slack action / notification step",
    "mail ": "plugin -> notification step",
    "junit": "test report -> upload-artifact / test reporter",
}


def find_jenkinsfiles(folder):
    found = []
    for root, dirs, files in os.walk(folder):
        for name in files:
            if name == "Jenkinsfile":
                found.append(os.path.join(root, name))
    return found


def analyse(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    stages = re.findall(r"stage\('([^']+)'\)", text)
    notes = []
    for keyword, advice in RISKY_ITEMS.items():
        if keyword in text:
            notes.append(advice)

    uses_docker = "docker" in text.lower()
    uses_k8s = "kubectl" in text or "helm" in text

    return {
        "file": path,
        "stages": stages,
        "docker": uses_docker,
        "kubernetes": uses_k8s,
        "notes": notes,
    }


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    files = find_jenkinsfiles(folder)
    print(f"Found {len(files)} Jenkinsfile(s) in '{folder}'\n")

    for path in files:
        result = analyse(path)
        print("=" * 60)
        print("Pipeline :", result["file"])
        print("Stages   :", ", ".join(result["stages"]))
        print("Docker   :", "yes" if result["docker"] else "no")
        print("K8s      :", "yes" if result["kubernetes"] else "no")

        # Suggest which golden-path template fits
        template = "reusable-python-ci"
        if result["docker"]:
            template += " + reusable-docker-build"
        if result["kubernetes"]:
            template += " + reusable-k8s-deploy"
        print("Template :", template)

        print("Needs attention:")
        for note in result["notes"]:
            print("   -", note)
    print("=" * 60)


if __name__ == "__main__":
    main()
