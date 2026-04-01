"""
Report Completeness Checker — flags reports missing required sections per RULES.md.

Checks:
- Header fields (Date, Test Plan, Environment)
- Summary table
- Per-TC: Result, URL, Steps, Assertions, Screenshots
- All tabs checked (Client Info, Loan Info, Farms)
- Toast/status assertions after state changes
- No skipped steps

Usage:
    py reporting/report-completeness.py
    py reporting/report-completeness.py test-reports/personal-loan/personal-loan-2026-03-19T15-18.md

Output: reporting/metrics/completeness-report.md
"""

import re
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "test-reports"
OUTPUT_FILE = PROJECT_ROOT / "reporting" / "metrics" / "completeness-report.md"


def check_report(filepath: Path) -> dict:
    """Check a report for completeness against RULES.md requirements."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    checks = {
        "file": filepath.name,
        "module": filepath.parent.name,
        "path": str(filepath.relative_to(PROJECT_ROOT)),
        "issues": [],
        "warnings": [],
        "score": 0,
        "max_score": 0,
    }

    def require(condition: bool, label: str):
        checks["max_score"] += 1
        if condition:
            checks["score"] += 1
        else:
            checks["issues"].append(label)

    def warn(condition: bool, label: str):
        if not condition:
            checks["warnings"].append(label)

    # --- Header checks ---
    has_date = any("**Date:**" in l for l in lines[:10])
    has_plan = any("**Test Plan:**" in l for l in lines[:10])
    has_env = any("**Environment:**" in l for l in lines[:15])
    has_title = any(l.startswith("# ") for l in lines[:3])

    require(has_title, "Missing report title (# heading)")
    require(has_date, "Missing **Date:** field")
    require(has_plan, "Missing **Test Plan:** field")
    require(has_env, "Missing **Environment:** field")

    # --- Summary table ---
    has_summary = bool(re.search(
        r"\|\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|", content
    )) or bool(re.search(r"Total cases\s*\|\s*\d+", content))
    require(has_summary, "Missing summary table (Total/Pass/Fail/Skip)")

    # --- Per-TC checks ---
    tc_sections = re.split(r"(?=^## TC-)", content, flags=re.MULTILINE)
    tc_count = 0

    for section in tc_sections:
        if not section.startswith("## TC-"):
            continue
        tc_count += 1

        tc_match = re.match(r"## (TC-\S+): (.+)", section)
        tc_id = tc_match.group(1) if tc_match else "Unknown"

        # Result line
        has_result = bool(re.search(r"\*\*Result:?\*\*\s*\w+", section))
        require(has_result, f"{tc_id}: Missing **Result** line")

        # URL
        has_url = bool(re.search(r"\*\*URL:\*\*", section))
        require(has_url, f"{tc_id}: Missing **URL** field")

        # Steps Followed
        has_steps = "### Steps Followed" in section or "### Steps" in section
        require(has_steps, f"{tc_id}: Missing ### Steps Followed section")

        # Steps content (numbered list)
        step_count = len(re.findall(r"^\d+\.\s+", section, re.MULTILINE))
        require(step_count > 0, f"{tc_id}: No numbered steps found")

        # Assertions section
        has_assertions = "### Assertions" in section or "- [x]" in section or "- [!]" in section
        require(has_assertions, f"{tc_id}: Missing assertions")

        # At least one assertion checked
        assertion_count = len(re.findall(r"- \[x\]|\- \[!\]", section))
        require(assertion_count > 0, f"{tc_id}: No assertions checked (need [x] or [!])")

        # Screenshot reference (warning, not required for all TCs)
        has_screenshot = bool(re.search(r"tc\d+.*\.png|!\[.+\]\(.+\.png\)|### Snapshots", section, re.IGNORECASE))
        warn(has_screenshot, f"{tc_id}: No screenshot referenced")

        # Toast assertions after state-changing actions
        state_changing = any(kw in section.lower() for kw in [
            "initiate", "submit", "save", "finalise", "finalize", "approve",
        ])
        has_toast = bool(re.search(r"toast|\"[^\"]+successfully|\"[^\"]+passed", section, re.IGNORECASE))
        if state_changing:
            require(has_toast, f"{tc_id}: State-changing action without toast/status assertion")

        # Status badge assertion after key actions
        if any(kw in section.lower() for kw in ["initiate loan", "consent", "verification"]):
            has_status = bool(re.search(r"status.*:|badge|consent pending|verification in progress|draft|resolution pending", section, re.IGNORECASE))
            require(has_status, f"{tc_id}: Missing status badge assertion after key action")

    require(tc_count > 0, "No test case sections (## TC-XX) found")

    # --- Tab coverage (for opportunity detail reports) ---
    if "opportunity" in content.lower() or "client info" in content.lower():
        has_client_tab = "client info" in content.lower()
        has_loan_tab = "loan info" in content.lower()
        has_farms_tab = "farms" in content.lower() or "farm" in content.lower()
        warn(has_client_tab, "No Client Info tab mentioned")
        warn(has_loan_tab, "No Loan Info tab mentioned")
        warn(has_farms_tab, "No Farms tab mentioned")

    # --- Test Data Summary ---
    has_test_data = "## Test Data" in content or "### Test Data" in content
    warn(has_test_data, "No Test Data Summary section")

    return checks


def generate_report(all_checks: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")

    lines = [
        "# Report Completeness Check",
        f"**Generated:** {now}",
        "",
        "---",
        "",
    ]

    # Summary
    total_reports = len(all_checks)
    perfect = [c for c in all_checks if not c["issues"]]
    with_issues = [c for c in all_checks if c["issues"]]

    avg_score = sum(c["score"] for c in all_checks) / total_reports if total_reports else 0
    avg_max = sum(c["max_score"] for c in all_checks) / total_reports if total_reports else 0
    avg_pct = round(avg_score / avg_max * 100, 1) if avg_max else 0

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Reports checked | {total_reports} |")
    lines.append(f"| Perfect (no issues) | {len(perfect)} |")
    lines.append(f"| With issues | **{len(with_issues)}** |")
    lines.append(f"| Average completeness | {avg_pct}% |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Scorecard
    lines.append("## Scorecard")
    lines.append("")
    lines.append("| Report | Module | Score | Issues | Warnings |")
    lines.append("|--------|--------|-------|--------|----------|")
    for c in sorted(all_checks, key=lambda x: x["score"] / max(x["max_score"], 1)):
        pct = round(c["score"] / c["max_score"] * 100) if c["max_score"] else 0
        lines.append(
            f"| {c['file']} | {c['module']} | "
            f"{c['score']}/{c['max_score']} ({pct}%) | "
            f"{len(c['issues'])} | {len(c['warnings'])} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed issues
    if with_issues:
        lines.append("## Issues by Report")
        lines.append("")
        for c in sorted(with_issues, key=lambda x: len(x["issues"]), reverse=True):
            pct = round(c["score"] / c["max_score"] * 100) if c["max_score"] else 0
            lines.append(f"### {c['file']} ({pct}%)")
            lines.append(f"**Path:** {c['path']}")
            lines.append("")
            for issue in c["issues"]:
                lines.append(f"- {issue}")
            if c["warnings"]:
                lines.append("")
                lines.append("**Warnings:**")
                for w in c["warnings"]:
                    lines.append(f"- {w}")
            lines.append("")

    # Common issues
    all_issues = []
    for c in all_checks:
        all_issues.extend(c["issues"])

    if all_issues:
        # Group by issue type (strip TC prefix)
        issue_types = {}
        for issue in all_issues:
            # Remove TC-XX: prefix
            clean = re.sub(r"^TC-\S+:\s*", "", issue)
            issue_types[clean] = issue_types.get(clean, 0) + 1

        lines.append("---")
        lines.append("")
        lines.append("## Most Common Issues")
        lines.append("")
        lines.append("| Issue | Count |")
        lines.append("|-------|-------|")
        for issue, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True)[:15]:
            lines.append(f"| {issue} | {count} |")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        report_files = [Path(sys.argv[1]).resolve()]
    else:
        report_files = sorted(REPORTS_DIR.rglob("*.md"))

    all_checks = []
    for f in report_files:
        result = check_report(f)
        pct = round(result["score"] / result["max_score"] * 100) if result["max_score"] else 0
        status = "OK" if not result["issues"] else f"{len(result['issues'])} issues"
        print(f"  {result['file']}: {pct}% ({status})")
        all_checks.append(result)

    report = generate_report(all_checks)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    total_issues = sum(len(c["issues"]) for c in all_checks)
    print(f"\n{len(all_checks)} reports checked, {total_issues} total issues found")
    print(f"Report saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
