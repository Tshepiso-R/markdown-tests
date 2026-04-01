"""
Collects test metrics from markdown reports into a JSON file for Grafana.

Usage:
    py reporting/collect-metrics.py                # process all reports
    py reporting/collect-metrics.py <report.md>    # process single report

Output: reporting/metrics/test-metrics.json
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
METRICS_FILE = PROJECT_ROOT / "reporting" / "metrics" / "test-metrics.json"


def parse_summary(filepath: Path) -> dict | None:
    """Extract summary metrics from a markdown test report."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    meta = {
        "file": str(filepath.relative_to(PROJECT_ROOT)),
        "module": filepath.parent.name,
        "date": "",
        "title": "",
        "environment": "",
        "test_plan": "",
        "total": 0,
        "pass": 0,
        "fail": 0,
        "skip": 0,
        "blocked": 0,
        "pass_rate": 0.0,
        "issues": [],
        "test_cases": [],
    }

    # Parse header
    for line in lines[:10]:
        if line.startswith("# Test Report:"):
            meta["title"] = line.replace("# Test Report:", "").strip()
        elif line.startswith("**Date:**"):
            meta["date"] = line.replace("**Date:**", "").strip()
        elif line.startswith("**Test Plan:**"):
            meta["test_plan"] = line.replace("**Test Plan:**", "").strip()
        elif line.startswith("**Environment:**"):
            meta["environment"] = line.replace("**Environment:**", "").strip()

    # Parse summary table
    summary_pattern = re.compile(r"\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|")
    for line in lines:
        m = summary_pattern.match(line)
        if m:
            meta["total"] = int(m.group(1))
            meta["pass"] = int(m.group(2))
            meta["fail"] = int(m.group(3))
            meta["skip"] = int(m.group(4))
            meta["blocked"] = int(m.group(5))
            break

    # Pre-parse: extract results from summary tables (CI report format)
    summary_results = {}
    summary_table_pattern = re.compile(
        r"\|\s*(TC-\d+\w*)\s*\|\s*(.+?)\s*\|\s*(PASS\*?|FAIL\*?|SKIP|BLOCKED)\s*\|"
    )
    for line in lines:
        m = summary_table_pattern.match(line)
        if m:
            summary_results[m.group(1)] = m.group(3).rstrip("*").upper()

    # Parse individual test cases
    tc_pattern = re.compile(r"^## (TC-\d+\w*): (.+)$")
    result_pattern = re.compile(r"^\*\*Result:?\*\*\s*(\w+)")
    issue_pattern = re.compile(r"^- \[!\] \*\*(.+?)\*\*")

    current_tc = None
    for line in lines:
        tc_match = tc_pattern.match(line)
        if tc_match:
            if current_tc:
                meta["test_cases"].append(current_tc)
            current_tc = {
                "id": tc_match.group(1),
                "name": tc_match.group(2),
                "result": "UNKNOWN",
            }
            continue

        if current_tc:
            result_match = result_pattern.match(line)
            if result_match:
                current_tc["result"] = result_match.group(1).upper()

        issue_match = issue_pattern.match(line)
        if issue_match:
            meta["issues"].append(issue_match.group(1))

    if current_tc:
        meta["test_cases"].append(current_tc)

    # Backfill results from summary table
    for tc in meta["test_cases"]:
        if tc["result"] == "UNKNOWN" and tc["id"] in summary_results:
            tc["result"] = summary_results[tc["id"]]

    # Fallback: count from individual TCs if summary table missing
    if meta["total"] == 0 and meta["test_cases"]:
        meta["total"] = len(meta["test_cases"])
        meta["pass"] = sum(1 for tc in meta["test_cases"] if tc["result"] == "PASS")
        meta["fail"] = sum(1 for tc in meta["test_cases"] if tc["result"] == "FAIL")
        meta["skip"] = sum(1 for tc in meta["test_cases"] if tc["result"] == "SKIP")
        meta["blocked"] = sum(1 for tc in meta["test_cases"] if tc["result"] == "BLOCKED")

    if meta["total"] > 0:
        meta["pass_rate"] = round(meta["pass"] / meta["total"] * 100, 1)

    # Need at least a date and some test cases
    if not meta["date"] or meta["total"] == 0:
        return None

    return meta


def load_existing_metrics() -> list[dict]:
    """Load existing metrics file or return empty list."""
    if METRICS_FILE.exists():
        return json.loads(METRICS_FILE.read_text(encoding="utf-8"))
    return []


def save_metrics(metrics: list[dict]):
    """Save metrics, sorted by date."""
    metrics.sort(key=lambda m: m.get("date", ""))
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    METRICS_FILE.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def main():
    reports_dir = PROJECT_ROOT / "test-reports"

    if len(sys.argv) > 1 and sys.argv[1] != "--all":
        report_files = [Path(sys.argv[1])]
    else:
        report_files = sorted(reports_dir.rglob("*.md"))

    existing = load_existing_metrics()
    existing_files = {m["file"] for m in existing}

    new_count = 0
    for report_path in report_files:
        rel_path = str(report_path.relative_to(PROJECT_ROOT))
        if rel_path in existing_files:
            print(f"  Skip (already indexed): {report_path.name}")
            continue

        result = parse_summary(report_path)
        if result:
            existing.append(result)
            new_count += 1
            tc_summary = f"{result['pass']}P/{result['fail']}F/{result['skip']}S"
            print(f"  Added: {report_path.name} [{tc_summary}] ({result['pass_rate']}%)")
        else:
            print(f"  Skip (no data): {report_path.name}")

    save_metrics(existing)
    print(f"\n{new_count} new report(s) added. Total: {len(existing)} reports.")
    print(f"Metrics saved to: {METRICS_FILE}")


if __name__ == "__main__":
    main()
