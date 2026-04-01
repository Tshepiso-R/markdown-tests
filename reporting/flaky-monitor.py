"""
Flaky Test Monitor — detects tests that flip between PASS/FAIL across runs.

Usage:
    py reporting/flaky-monitor.py              # analyze all reports
    py reporting/flaky-monitor.py --module personal-loan   # filter by module

Output: reporting/metrics/flaky-report.md
"""

import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "test-reports"
OUTPUT_FILE = PROJECT_ROOT / "reporting" / "metrics" / "flaky-report.md"


def parse_test_results(filepath: Path) -> list[dict]:
    """Extract test case ID, name, and result from a report."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    date = ""
    module = filepath.parent.name

    for line in lines[:10]:
        if line.startswith("**Date:**"):
            date = line.replace("**Date:**", "").strip()

    # Extract from summary tables (CI format)
    summary_results = {}
    summary_table = re.compile(
        r"\|\s*(TC-\d+\w*)\s*\|\s*(.+?)\s*\|\s*(PASS\*?|FAIL\*?|SKIP|BLOCKED)\s*\|"
    )
    for line in lines:
        m = summary_table.match(line)
        if m:
            summary_results[m.group(1)] = {
                "name": m.group(2).strip(),
                "result": m.group(3).rstrip("*").upper(),
            }

    # Extract from inline TC sections
    tc_pattern = re.compile(r"^## (TC-\d+\w*): (.+)$")
    result_pattern = re.compile(r"^\*\*Result:?\*\*\s*(\w+)")

    results = []
    current_id = None
    current_name = None

    for line in lines:
        tc_match = tc_pattern.match(line)
        if tc_match:
            current_id = tc_match.group(1)
            current_name = tc_match.group(2)
            continue

        if current_id:
            result_match = result_pattern.match(line)
            if result_match:
                results.append({
                    "id": current_id,
                    "name": current_name,
                    "result": result_match.group(1).upper(),
                    "date": date,
                    "file": filepath.name,
                    "module": module,
                })
                current_id = None
                current_name = None

    # Backfill from summary table
    found_ids = {r["id"] for r in results}
    for tc_id, info in summary_results.items():
        if tc_id not in found_ids:
            results.append({
                "id": tc_id,
                "name": info["name"],
                "result": info["result"],
                "date": date,
                "file": filepath.name,
                "module": module,
            })
        else:
            # Fill in result for TCs that had UNKNOWN
            for r in results:
                if r["id"] == tc_id and r["result"] == "UNKNOWN":
                    r["result"] = info["result"]

    return results


def analyze_flakiness(all_results: list[dict], module_filter: str = None) -> dict:
    """Group results by test case and detect flakiness."""
    # Group by normalized key: module + tc_id
    grouped = defaultdict(list)

    for r in all_results:
        if module_filter and r["module"] != module_filter:
            continue
        key = f"{r['module']}/{r['id']}"
        grouped[key].append(r)

    analysis = {
        "flaky": [],       # mixed PASS/FAIL
        "always_pass": [],
        "always_fail": [],
        "insufficient": [], # only 1 run
    }

    for key, runs in sorted(grouped.items()):
        # Only consider runs with definitive results
        definitive = [r for r in runs if r["result"] in ("PASS", "FAIL")]
        if len(definitive) < 2:
            analysis["insufficient"].append({
                "key": key,
                "name": runs[0]["name"],
                "runs": len(definitive),
                "history": runs,
            })
            continue

        results_set = {r["result"] for r in definitive}

        if results_set == {"PASS", "FAIL"}:
            pass_count = sum(1 for r in definitive if r["result"] == "PASS")
            fail_count = sum(1 for r in definitive if r["result"] == "FAIL")
            flake_rate = round(min(pass_count, fail_count) / len(definitive) * 100, 1)

            analysis["flaky"].append({
                "key": key,
                "name": definitive[0]["name"],
                "pass_count": pass_count,
                "fail_count": fail_count,
                "total": len(definitive),
                "flake_rate": flake_rate,
                "history": sorted(definitive, key=lambda r: r["date"]),
            })
        elif results_set == {"PASS"}:
            analysis["always_pass"].append({
                "key": key,
                "name": definitive[0]["name"],
                "total": len(definitive),
            })
        elif results_set == {"FAIL"}:
            analysis["always_fail"].append({
                "key": key,
                "name": definitive[0]["name"],
                "total": len(definitive),
            })

    # Sort flaky by flake rate descending
    analysis["flaky"].sort(key=lambda x: x["flake_rate"], reverse=True)

    return analysis


def generate_report(analysis: dict, module_filter: str = None) -> str:
    """Generate a markdown flaky test report."""
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    scope = f" ({module_filter})" if module_filter else ""

    lines = [
        f"# Flaky Test Monitor{scope}",
        f"**Generated:** {now}",
        "",
        "---",
        "",
    ]

    # Summary
    total_tracked = (
        len(analysis["flaky"])
        + len(analysis["always_pass"])
        + len(analysis["always_fail"])
        + len(analysis["insufficient"])
    )

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Category | Count |")
    lines.append(f"|----------|-------|")
    lines.append(f"| Flaky (mixed pass/fail) | **{len(analysis['flaky'])}** |")
    lines.append(f"| Always Pass | {len(analysis['always_pass'])} |")
    lines.append(f"| Always Fail | {len(analysis['always_fail'])} |")
    lines.append(f"| Insufficient Data (<2 runs) | {len(analysis['insufficient'])} |")
    lines.append(f"| **Total Tracked** | **{total_tracked}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Flaky tests (the main event)
    if analysis["flaky"]:
        lines.append("## Flaky Tests")
        lines.append("")
        lines.append("> These tests have flipped between PASS and FAIL across runs. Higher flake rate = more inconsistent.")
        lines.append("")

        for tc in analysis["flaky"]:
            lines.append(f"### {tc['key']}: {tc['name']}")
            lines.append(f"**Flake Rate:** {tc['flake_rate']}% | **Pass:** {tc['pass_count']} | **Fail:** {tc['fail_count']} | **Runs:** {tc['total']}")
            lines.append("")
            lines.append("| Date | Report | Result |")
            lines.append("|------|--------|--------|")
            for run in tc["history"]:
                icon = "PASS" if run["result"] == "PASS" else "**FAIL**"
                lines.append(f"| {run['date']} | {run['file']} | {icon} |")
            lines.append("")

        lines.append("---")
        lines.append("")
    else:
        lines.append("## Flaky Tests")
        lines.append("")
        lines.append("No flaky tests detected. All tests with 2+ runs are consistent.")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Always failing
    if analysis["always_fail"]:
        lines.append("## Always Failing")
        lines.append("")
        lines.append("> These tests have never passed. They may indicate real bugs or broken test setup.")
        lines.append("")
        lines.append("| Test Case | Name | Runs |")
        lines.append("|-----------|------|------|")
        for tc in analysis["always_fail"]:
            lines.append(f"| {tc['key']} | {tc['name']} | {tc['total']} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Always passing
    if analysis["always_pass"]:
        lines.append("## Always Passing")
        lines.append("")
        lines.append("| Test Case | Name | Runs |")
        lines.append("|-----------|------|------|")
        for tc in analysis["always_pass"]:
            lines.append(f"| {tc['key']} | {tc['name']} | {tc['total']} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Insufficient data
    if analysis["insufficient"]:
        lines.append("## Insufficient Data")
        lines.append("")
        lines.append("> These tests have fewer than 2 definitive runs. Need more data to determine stability.")
        lines.append("")
        lines.append("| Test Case | Name | Runs |")
        lines.append("|-----------|------|------|")
        for tc in analysis["insufficient"]:
            lines.append(f"| {tc['key']} | {tc['name']} | {tc['runs']} |")
        lines.append("")

    return "\n".join(lines)


def main():
    module_filter = None
    if "--module" in sys.argv:
        idx = sys.argv.index("--module")
        if idx + 1 < len(sys.argv):
            module_filter = sys.argv[idx + 1]

    # Parse all reports
    report_files = sorted(REPORTS_DIR.rglob("*.md"))
    all_results = []

    for f in report_files:
        results = parse_test_results(f)
        if results:
            all_results.append((f.name, len(results)))
            all_results_flat = []

    # Re-parse into flat list
    all_flat = []
    for f in report_files:
        all_flat.extend(parse_test_results(f))

    print(f"Parsed {len(report_files)} report files, {len(all_flat)} test case results")

    # Analyze
    analysis = analyze_flakiness(all_flat, module_filter)

    # Generate report
    report = generate_report(analysis, module_filter)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    # Print summary
    print(f"\nFlaky:        {len(analysis['flaky'])}")
    print(f"Always Pass:  {len(analysis['always_pass'])}")
    print(f"Always Fail:  {len(analysis['always_fail'])}")
    print(f"Need Data:    {len(analysis['insufficient'])}")
    print(f"\nReport saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
