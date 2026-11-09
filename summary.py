import json
from findings import load_bandit, count_by_severity
from deps import load_dependency_findings

def summary():
    code = load_bandit()
    deps = load_dependency_findings()
    return {
        "code_findings": len(code),
        "code_by_severity": count_by_severity(code),
        "vulnerable_packages": len(deps),
        "dependency_issues": [
            f"{d['package']} {d['version']}: {d['id']}" for d in deps
        ],
    }

if __name__ == "__main__":
    print(json.dumps(summary(), indent=2))