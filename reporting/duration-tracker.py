"""
Test Duration Tracker — extracts and trends execution time across runs.

Usage:
    py reporting/duration-tracker.py

Output: reporting/metrics/duration-report.md
"""

import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "test-reports"
OUTPUT_FILE = PROJECT_ROOT / "reporting" / "metrics" / "duration-report.md"


def parse_duration(filepath: Path) -> dict | None:
    """Extract duration info from a report."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    meta = {
        "file": filepath.name,
        "module": filepath.parent.name,
        "date": "",
        "title": "",
        "total_duration": None,
        "total_tests": 0,
        "tc_count": 0,
    }

    for line in lines[:15]:
        if line.startswith("# "):
            meta["title"] = line.lstrip("# ").strip()
        elif "**Date:**" in line:
            meta["date"] = line.split("**Date:**")[1].strip()

    # Look for duration in summary table
    for line in lines:
        # Match: | Duration | ~20m | or | Duration | ~1h 15m |
        dur_match = re.search(r"[Dd]uration\s*\|\s*~?(\d+)\s*([hm])", line)
        if dur_match:
            val = int(dur_match.group(1))
            unit = dur_match.group(2)
            meta["total_duration"] = val * 60 if unit == "h" else val
            break

    # Count TCs
    tc_pattern = re.compile(r"^## (TC-\d+\w*)")
    for line in lines:
        if tc_pattern.match(line):
            meta["tc_count"] += 1

    # Parse summary table for total tests
    summary_pattern = re.compile(r"\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|")
    for line in lines:
        m = summary_pattern.match(line)
        if m:
            meta["total_tests"] = int(m.group(1))
            break

    # Fallback: total cases from key-value table
    if meta["total_tests"] == 0:
        for line in lines:
            m = re.search(r"Total cases\s*\|\s*(\d+)", line)
            if m:
                meta["total_tests"] = int(m.group(1))
                break

    if meta["total_tests"] == 0:
        meta["total_tests"] = meta["tc_count"]

    if not meta["date"] or meta["total_tests"] == 0:
        return None

    # Estimate per-TC duration
    if meta["total_duration"] and meta["total_tests"] > 0:
        meta["avg_per_tc"] = round(meta["total_duration"] / meta["total_tests"], 1)
    else:
        meta["avg_per_tc"] = None

    return meta


def generate_report(runs: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")

    lines = [
        "# Test Duration Tracker",
        f"**Generated:** {now}",
        "",
        "---",
        "",
    ]

    # Runs with duration data
    timed = [r for r in runs if r["total_duration"] is not None]
    untimed = [r for r in runs if r["total_duration"] is None]

    if timed:
        avg_duration = sum(r["total_duration"] for r in timed) / len(timed)
        avg_per_tc = sum(r["avg_per_tc"] for r in timed if r["avg_per_tc"]) / len(timed)
        fastest = min(timed, key=lambda r: r["total_duration"])
        slowest = max(timed, key=lambda r: r["total_duration"])

        lines.append("## Summary")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Runs with duration data | {len(timed)} |")
        lines.append(f"| Average run duration | **{avg_duration:.0f} min** |")
        lines.append(f"| Average per test case | **{avg_per_tc:.1f} min** |")
        lines.append(f"| Fastest run | {fastest['file']} ({fastest['total_duration']} min) |")
        lines.append(f"| Slowest run | {slowest['file']} ({slowest['total_duration']} min) |")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Duration trend
        lines.append("## Duration Trend")
        lines.append("")
        lines.append("| Date | Module | Report | Duration | TCs | Avg/TC |")
        lines.append("|------|--------|--------|----------|-----|--------|")
        for r in sorted(timed, key=lambda x: x["date"]):
            avg = f"{r['avg_per_tc']:.1f} min" if r["avg_per_tc"] else "—"
            lines.append(
                f"| {r['date']} | {r['module']} | {r['file']} | "
                f"{r['total_duration']} min | {r['total_tests']} | {avg} |"
            )
        lines.append("")

        # Performance alerts
        lines.append("---")
        lines.append("")
        lines.append("## Performance Alerts")
        lines.append("")

        slow_runs = [r for r in timed if r["avg_per_tc"] and r["avg_per_tc"] > 3.0]
        if slow_runs:
            lines.append("> Runs where average per-TC exceeds 3 minutes:")
            lines.append("")
            for r in slow_runs:
                lines.append(f"- **{r['file']}** — {r['avg_per_tc']:.1f} min/TC ({r['module']})")
            lines.append("")
        else:
            lines.append("No slow runs detected (threshold: >3 min per TC).")
            lines.append("")
    else:
        lines.append("## No Duration Data")
        lines.append("")
        lines.append("None of the reports include execution duration. Add `| Duration | ~Xm |` to your report summary tables.")
        lines.append("")

    if untimed:
        lines.append("---")
        lines.append("")
        lines.append("## Reports Missing Duration")
        lines.append("")
        lines.append("| Date | Module | Report |")
        lines.append("|------|--------|--------|")
        for r in sorted(untimed, key=lambda x: x["date"]):
            lines.append(f"| {r['date']} | {r['module']} | {r['file']} |")
        lines.append("")

    return "\n".join(lines)


def main():
    report_files = sorted(REPORTS_DIR.rglob("*.md"))
    runs = []

    for f in report_files:
        result = parse_duration(f)
        if result:
            dur = f"{result['total_duration']}m" if result["total_duration"] else "no data"
            print(f"  {result['file']}: {result['total_tests']} TCs, {dur}")
            runs.append(result)

    report = generate_report(runs)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    print(f"\n{len(runs)} reports analyzed")
    timed = [r for r in runs if r["total_duration"]]
    print(f"{len(timed)} with duration data, {len(runs) - len(timed)} missing duration")
    print(f"Report saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
