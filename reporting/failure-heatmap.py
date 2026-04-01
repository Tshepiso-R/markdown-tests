"""
Failure Heatmap — identifies which TCs and phases fail most often.

Usage:
    py reporting/failure-heatmap.py

Output: reporting/metrics/failure-heatmap.md
"""

import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "test-reports"
OUTPUT_FILE = PROJECT_ROOT / "reporting" / "metrics" / "failure-heatmap.md"


def parse_all_results() -> list[dict]:
    """Parse all reports and extract per-TC results with failure details."""
    all_results = []

    for filepath in sorted(REPORTS_DIR.rglob("*.md")):
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")

        date = ""
        module = filepath.parent.name

        for line in lines[:10]:
            if "**Date:**" in line:
                date = line.split("**Date:**")[1].strip()

        # Summary table results
        summary = {}
        for line in lines:
            m = re.match(r"\|\s*(TC-\d+\w*)\s*\|\s*(.+?)\s*\|\s*(PASS\*?|FAIL\*?|SKIP|BLOCKED)\s*\|", line)
            if m:
                summary[m.group(1)] = m.group(3).rstrip("*").upper()

        # Inline TC results
        tc_pattern = re.compile(r"^## (TC-\d+\w*): (.+)$")
        result_pattern = re.compile(r"^\*\*Result:?\*\*\s*(\w+)")
        assertion_fail = re.compile(r"^- \[!\] (.+)")
        issue_pattern = re.compile(r"### Issue|### Issues")

        current_tc = None
        current_name = None
        current_result = None
        current_failures = []
        in_issue = False

        for line in lines:
            tc_match = tc_pattern.match(line)
            if tc_match:
                # Save previous
                if current_tc:
                    result = current_result or summary.get(current_tc, "UNKNOWN")
                    all_results.append({
                        "tc": current_tc,
                        "name": current_name,
                        "result": result,
                        "failures": current_failures[:],
                        "module": module,
                        "date": date,
                        "file": filepath.name,
                    })
                current_tc = tc_match.group(1)
                current_name = tc_match.group(2)
                current_result = None
                current_failures = []
                in_issue = False
                continue

            if current_tc:
                rm = result_pattern.match(line)
                if rm:
                    current_result = rm.group(1).upper()

                fm = assertion_fail.match(line)
                if fm:
                    current_failures.append(fm.group(1))

                if issue_pattern.match(line):
                    in_issue = True
                elif in_issue and line.startswith("- "):
                    current_failures.append(line.lstrip("- ").strip())

        if current_tc:
            result = current_result or summary.get(current_tc, "UNKNOWN")
            all_results.append({
                "tc": current_tc,
                "name": current_name,
                "result": result,
                "failures": current_failures[:],
                "module": module,
                "date": date,
                "file": filepath.name,
            })

    return all_results


def generate_report(results: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")

    lines = [
        "# Failure Heatmap",
        f"**Generated:** {now}",
        "",
        "---",
        "",
    ]

    # Overall stats
    total = len(results)
    fails = [r for r in results if r["result"] == "FAIL"]
    passes = [r for r in results if r["result"] == "PASS"]
    skips = [r for r in results if r["result"] in ("SKIP", "BLOCKED")]
    issues = [r for r in results if r["failures"]]

    lines.append("## Overview")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total TC executions | {total} |")
    lines.append(f"| Passed | {len(passes)} |")
    lines.append(f"| Failed | **{len(fails)}** |")
    lines.append(f"| Skipped/Blocked | {len(skips)} |")
    lines.append(f"| Executions with issues flagged | {len(issues)} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Failure frequency by TC
    tc_fail_count = Counter()
    tc_total_count = Counter()
    tc_names = {}

    for r in results:
        key = f"{r['module']}/{r['tc']}"
        tc_total_count[key] += 1
        tc_names[key] = r["name"]
        if r["result"] == "FAIL":
            tc_fail_count[key] += 1

    lines.append("## Failure Frequency by Test Case")
    lines.append("")
    if tc_fail_count:
        lines.append("| Test Case | Name | Failures | Total Runs | Fail Rate |")
        lines.append("|-----------|------|----------|------------|-----------|")
        for key, count in tc_fail_count.most_common():
            total_runs = tc_total_count[key]
            rate = round(count / total_runs * 100, 1)
            lines.append(f"| {key} | {tc_names[key]} | **{count}** | {total_runs} | {rate}% |")
    else:
        lines.append("No test case failures recorded across all runs.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Failure frequency by module
    module_fails = Counter()
    module_totals = Counter()
    for r in results:
        module_totals[r["module"]] += 1
        if r["result"] == "FAIL":
            module_fails[r["module"]] += 1

    lines.append("## Failure Rate by Module")
    lines.append("")
    lines.append("| Module | Failures | Total | Fail Rate |")
    lines.append("|--------|----------|-------|-----------|")
    for module in sorted(module_totals.keys()):
        f_count = module_fails.get(module, 0)
        t_count = module_totals[module]
        rate = round(f_count / t_count * 100, 1) if t_count else 0
        lines.append(f"| {module} | {f_count} | {t_count} | {rate}% |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Failure by phase (derive from TC numbering)
    phase_map = {
        "01": "Lead Creation",
        "02": "Pre-Screening",
        "03": "Opportunity Setup",
        "04": "Loan Info",
        "05": "Initiate / Consent",
        "06": "Verification",
        "07": "Onboarding Checklist",
        "08": "Final Status",
    }
    phase_fails = Counter()
    phase_totals = Counter()
    for r in results:
        tc_num = re.match(r"TC-(\d+)", r["tc"])
        if tc_num:
            phase = phase_map.get(tc_num.group(1), f"Phase {tc_num.group(1)}")
            phase_totals[phase] += 1
            if r["result"] == "FAIL":
                phase_fails[phase] += 1

    lines.append("## Failure Rate by Phase")
    lines.append("")
    lines.append("| Phase | Failures | Total | Fail Rate | Heat |")
    lines.append("|-------|----------|-------|-----------|------|")
    for phase in phase_map.values():
        if phase in phase_totals:
            f_count = phase_fails.get(phase, 0)
            t_count = phase_totals[phase]
            rate = round(f_count / t_count * 100, 1)
            heat = "***" if rate > 30 else "**" if rate > 10 else "*" if rate > 0 else ""
            lines.append(f"| {phase} | {f_count} | {t_count} | {rate}% | {heat} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # All flagged issues
    if issues:
        lines.append("## All Flagged Issues")
        lines.append("")
        lines.append("| Date | Module | TC | Issue |")
        lines.append("|------|--------|----|-------|")
        for r in sorted(issues, key=lambda x: x["date"], reverse=True):
            for issue in r["failures"]:
                # Truncate long issues
                short = issue[:120] + "..." if len(issue) > 120 else issue
                lines.append(f"| {r['date']} | {r['module']} | {r['tc']} | {short} |")
        lines.append("")

    return "\n".join(lines)


def main():
    results = parse_all_results()
    print(f"Parsed {len(results)} TC executions across all reports")

    report = generate_report(results)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    fails = sum(1 for r in results if r["result"] == "FAIL")
    issues = sum(1 for r in results if r["failures"])
    print(f"Failures: {fails}, Issues flagged: {issues}")
    print(f"Report saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
