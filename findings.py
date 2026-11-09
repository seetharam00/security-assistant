import json
from pathlib import Path

def load_bandit(path="reports/bandit.json"):
    data = json.loads(Path(path).read_text())
    return [
        {
            "severity": r["issue_severity"],
            "file": r["filename"],
            "line": r["line_number"],
            "issue": r["issue_text"],
        }
        for r in data["results"]
    ]

def count_by_severity(findings):
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    return counts

if __name__ == "__main__":
    findings = load_bandit()
    print("Total:", len(findings))
    print("By severity:", count_by_severity(findings))
    for f in findings:
        print(f"[{f['severity']}] {f['file']}:{f['line']} {f['issue']}")