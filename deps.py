import json
from pathlib import Path

def load_dependency_findings(path="reports/pip-audit.json"):
    data = json.loads(Path(path).read_text())
    findings = []
    for dep in data["dependencies"]:
        for vuln in dep.get("vulns", []):
            findings.append({
                "package": dep["name"],
                "version": dep["version"],
                "id": vuln["id"],
                "fix_versions": vuln.get("fix_versions", []),
                "description": vuln.get("description", ""),
            })
    return findings

if __name__ == "__main__":
    findings = load_dependency_findings()
    print("Vulnerable packages:", len(findings))
    for f in findings:
        fix = ", ".join(f["fix_versions"]) or "no fix listed"
        print(f"{f['package']} {f['version']}: {f['id']} (fix: {fix})")