"""
Converts markdown test reports into Allure-compatible JSON results.

Usage:
    py reporting/convert-to-allure.py test-reports/personal-loan/personal-loan-2026-03-19T15-18.md
    py reporting/convert-to-allure.py --all          # converts all reports

Then generate the HTML report:
    allure generate reporting/allure-results -o reporting/allure-report --clean
    allure open reporting/allure-report
"""

import json
import re
import sys
import os
import uuid
import hashlib
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def parse_report(filepath: Path) -> dict:
    """Parse a markdown test report into structured data."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    report = {
        "title": "",
        "date": "",
        "test_plan": "",
        "environment": "",
        "module": filepath.parent.name,
        "test_cases": [],
    }

    # Parse header
    for line in lines[:10]:
        if line.startswith("# Test Report:"):
            report["title"] = line.replace("# Test Report:", "").strip()
        elif line.startswith("**Date:**"):
            report["date"] = line.replace("**Date:**", "").strip()
        elif line.startswith("**Test Plan:**"):
            report["test_plan"] = line.replace("**Test Plan:**", "").strip()
        elif line.startswith("**Environment:**"):
            report["environment"] = line.replace("**Environment:**", "").strip()

    # Pre-parse: extract results from summary tables (CI report format)
    # Matches: | TC-01 | Create Lead | PASS | ... |
    summary_results = {}
    summary_table_pattern = re.compile(
        r"\|\s*(TC-\d+\w*)\s*\|\s*(.+?)\s*\|\s*(PASS\*?|FAIL\*?|SKIP|BLOCKED)\s*\|"
    )
    for line in lines:
        m = summary_table_pattern.match(line)
        if m:
            tc_id = m.group(1)
            result_val = m.group(3).rstrip("*").upper()
            summary_results[tc_id] = result_val

    # Parse test cases
    tc_pattern = re.compile(r"^## (TC-\d+\w*): (.+)$")
    result_pattern = re.compile(r"^\*\*Result:?\*\*\s*(\w+)")
    url_pattern = re.compile(r"^\*\*URL:\*\*\s*(.+)")
    assertion_pass = re.compile(r"^- \[x\] (.+)")
    assertion_fail = re.compile(r"^- \[!\] (.+)")
    issue_pattern = re.compile(r"^- \[!\] \*\*(.+?)\*\*")

    current_tc = None
    in_steps = False
    in_assertions = False

    for line in lines:
        tc_match = tc_pattern.match(line)
        if tc_match:
            if current_tc:
                report["test_cases"].append(current_tc)
            current_tc = {
                "id": tc_match.group(1),
                "name": tc_match.group(2),
                "result": "UNKNOWN",
                "url": "",
                "steps": [],
                "assertions_pass": [],
                "assertions_fail": [],
                "issues": [],
            }
            in_steps = False
            in_assertions = False
            continue

        if current_tc is None:
            continue

        result_match = result_pattern.match(line)
        if result_match:
            current_tc["result"] = result_match.group(1).upper()
            continue

        url_match = url_pattern.match(line)
        if url_match:
            current_tc["url"] = url_match.group(1).strip()
            continue

        if "### Steps Followed" in line:
            in_steps = True
            in_assertions = False
            continue
        if "### Assertions" in line:
            in_assertions = True
            in_steps = False
            continue
        if line.startswith("### ") or line.startswith("## ") or line == "---":
            in_steps = False
            in_assertions = False

        if in_steps:
            step_match = re.match(r"^\d+\.\s+(.+)", line)
            if step_match:
                current_tc["steps"].append(step_match.group(1))

        pass_match = assertion_pass.match(line)
        if pass_match:
            current_tc["assertions_pass"].append(pass_match.group(1))

        fail_match = assertion_fail.match(line)
        if fail_match:
            current_tc["assertions_fail"].append(fail_match.group(1))

        issue_match = issue_pattern.match(line)
        if issue_match:
            current_tc["issues"].append(issue_match.group(1))

    if current_tc:
        report["test_cases"].append(current_tc)

    # Backfill results from summary table for TCs that didn't have inline results
    for tc in report["test_cases"]:
        if tc["result"] == "UNKNOWN" and tc["id"] in summary_results:
            tc["result"] = summary_results[tc["id"]]

    return report


def to_allure_results(report: dict, output_dir: Path):
    """Convert parsed report to Allure JSON result files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse timestamp
    try:
        dt = datetime.fromisoformat(report["date"])
        timestamp_ms = int(dt.timestamp() * 1000)
    except (ValueError, TypeError):
        timestamp_ms = int(datetime.now().timestamp() * 1000)

    for tc in report["test_cases"]:
        # Deterministic UUID from module + tc id
        test_id = hashlib.md5(f"{report['module']}/{tc['id']}".encode()).hexdigest()
        result_id = str(uuid.uuid4())

        status_map = {
            "PASS": "passed",
            "FAIL": "failed",
            "SKIP": "skipped",
            "BLOCKED": "skipped",
        }
        status = status_map.get(tc["result"], "broken")

        # Build steps
        allure_steps = []
        for i, step in enumerate(tc["steps"], 1):
            allure_steps.append({
                "name": f"Step {i}: {step}",
                "status": "passed" if tc["result"] == "PASS" else status,
                "stage": "finished",
            })

        # Build assertions as steps
        for assertion in tc["assertions_pass"]:
            allure_steps.append({
                "name": f"Assert: {assertion}",
                "status": "passed",
                "stage": "finished",
            })
        for assertion in tc["assertions_fail"]:
            allure_steps.append({
                "name": f"Assert: {assertion}",
                "status": "failed",
                "stage": "finished",
            })

        # Status details for failures
        status_details = {}
        if tc["assertions_fail"]:
            status_details["message"] = "; ".join(tc["assertions_fail"])
        if tc["issues"]:
            status_details["message"] = "; ".join(tc["issues"])

        allure_result = {
            "uuid": result_id,
            "historyId": test_id,
            "name": f"{tc['id']}: {tc['name']}",
            "fullName": f"{report['module']}.{tc['id']}",
            "status": status,
            "statusDetails": status_details,
            "stage": "finished",
            "steps": allure_steps,
            "start": timestamp_ms,
            "stop": timestamp_ms + 1000,
            "labels": [
                {"name": "suite", "value": report["title"] or report["module"]},
                {"name": "parentSuite", "value": report["module"]},
                {"name": "epic", "value": report["module"]},
                {"name": "feature", "value": tc["name"]},
                {"name": "host", "value": report["environment"]},
            ],
            "links": [],
            "parameters": [],
        }

        if tc["url"]:
            allure_result["links"].append({
                "name": "Test URL",
                "url": tc["url"],
                "type": "tms",
            })

        result_file = output_dir / f"{result_id}-result.json"
        result_file.write_text(json.dumps(allure_result, indent=2), encoding="utf-8")
        print(f"  -> {tc['id']}: {tc['name']} [{status}]")

    # Write environment.properties
    env_file = output_dir / "environment.properties"
    env_lines = [
        f"Environment={report['environment']}",
        f"TestPlan={report['test_plan']}",
        f"Module={report['module']}",
        f"Date={report['date']}",
    ]
    env_file.write_text("\n".join(env_lines), encoding="utf-8")


def find_all_reports() -> list[Path]:
    """Find all markdown test reports."""
    reports_dir = PROJECT_ROOT / "test-reports"
    return sorted(reports_dir.rglob("*.md"))


def main():
    output_dir = PROJECT_ROOT / "reporting" / "allure-results"

    if len(sys.argv) < 2:
        print("Usage:")
        print("  py reporting/convert-to-allure.py <report.md>")
        print("  py reporting/convert-to-allure.py --all")
        sys.exit(1)

    if sys.argv[1] == "--all":
        reports = find_all_reports()
        print(f"Found {len(reports)} report(s)")
    else:
        reports = [Path(sys.argv[1])]

    for report_path in reports:
        if not report_path.exists():
            print(f"Not found: {report_path}")
            continue
        print(f"\nConverting: {report_path.name}")
        report = parse_report(report_path)
        if report["test_cases"]:
            to_allure_results(report, output_dir)
            print(f"  {len(report['test_cases'])} test cases converted")
        else:
            print("  No test cases found, skipping")

    print(f"\nAllure results written to: {output_dir}")
    print("Next steps:")
    print("  1. Install Allure: npm install -g allure-commandline")
    print("  2. Generate report: allure generate reporting/allure-results -o reporting/allure-report --clean")
    print("  3. Open report:     allure open reporting/allure-report")


if __name__ == "__main__":
    main()
