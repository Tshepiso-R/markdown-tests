"""
Drift History Log — tracks when test plans changed vs when tests started failing.
Correlates git history of test plans with test report results.

Usage:
    py reporting/drift-history.py

Output: reporting/metrics/drift-history.md
"""

import re
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "test-reports"
PLANS_DIR = PROJECT_ROOT / "test-plans"
OUTPUT_FILE = PROJECT_ROOT / "reporting" / "metrics" / "drift-history.md"


def get_git_log(filepath: Path) -> list[dict]:
    """Get git commit history for a file."""
    try:
        result = subprocess.run(
            ["git", "log", "--format=%H|%ai|%s", "--follow", str(filepath)],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        commits = []
        for line in result.stdout.strip().split("\n"):
            if "|" in line:
                parts = line.split("|", 2)
                commits.append({
                    "hash": parts[0][:8],
                    "date": parts[1].strip()[:10],
                    "message": parts[2].strip(),
                })
        return commits
    except Exception:
        return []


def parse_report_results(filepath: Path) -> dict | None:
    """Extract date and pass/fail from a report."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    date = ""
    module = filepath.parent.name
    total = 0
    passed = 0
    failed = 0

    for line in lines[:10]:
        if "**Date:**" in line:
            date = line.split("**Date:**")[1].strip()

    # Summary table
    for line in lines:
        m = re.match(r"\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
        if m:
            total, passed, failed = int(m.group(1)), int(m.group(2)), int(m.group(3))
            break

    # Key-value summary
    if total == 0:
        for line in lines:
            m = re.search(r"Total cases\s*\|\s*(\d+)", line)
            if m:
                total = int(m.group(1))
            m = re.search(r"Passed\s*\|\s*(\d+)", line)
            if m:
                passed = int(m.group(1))
            m = re.search(r"Failed\s*\|\s*(\d+)", line)
            if m:
                failed = int(m.group(1))

    # Count from summary table rows
    if total == 0:
        for line in lines:
            m = re.match(r"\|\s*TC-\d+\w*\s*\|.+\|\s*(PASS\*?|FAIL\*?)\s*\|", line)
            if m:
                total += 1
                if "PASS" in m.group(1):
                    passed += 1
                else:
                    failed += 1

    if not date or total == 0:
        return None

    # Detect drift notes
    has_drift = False
    drift_notes = []
    for line in lines:
        if "changes detected" in line.lower() or "drift" in line.lower() or "suggested update" in line.lower():
            has_drift = True
        if "suggested update" in line.lower() or "discrepancy" in line.lower():
            drift_notes.append(line.strip().lstrip("- "))

    return {
        "file": filepath.name,
        "module": module,
        "date": date[:10],
        "total": total,
        "passed": passed,
        "failed": failed,
        "has_drift": has_drift,
        "drift_notes": drift_notes[:5],
    }


def generate_report(plan_history: dict, run_results: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")

    lines = [
        "# Drift History Log",
        f"**Generated:** {now}",
        "",
        "> Correlates test plan changes (git history) with test run results to identify",
        "> whether plan edits coincide with test failures or regressions.",
        "",
        "---",
        "",
    ]

    # Timeline: merge plan edits and test runs
    events = []

    for plan_name, commits in plan_history.items():
        for c in commits:
            events.append({
                "date": c["date"],
                "type": "PLAN EDIT",
                "source": plan_name,
                "detail": c["message"],
                "hash": c["hash"],
            })

    for r in run_results:
        status = "PASS" if r["failed"] == 0 else f"FAIL ({r['failed']}/{r['total']})"
        drift_flag = " [DRIFT]" if r["has_drift"] else ""
        events.append({
            "date": r["date"],
            "type": "TEST RUN",
            "source": r["module"],
            "detail": f"{status}{drift_flag} — {r['file']}",
            "hash": "",
        })

    events.sort(key=lambda e: e["date"])

    # Full timeline
    lines.append("## Timeline")
    lines.append("")
    lines.append("| Date | Event | Source | Detail |")
    lines.append("|------|-------|--------|--------|")
    for e in events:
        hash_ref = f" `{e['hash']}`" if e["hash"] else ""
        lines.append(f"| {e['date']} | {e['type']} | {e['source']} | {e['detail']}{hash_ref} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Plan edit summary
    lines.append("## Test Plan Change History")
    lines.append("")
    for plan_name, commits in sorted(plan_history.items()):
        lines.append(f"### {plan_name}")
        lines.append(f"**Total edits:** {len(commits)}")
        lines.append("")
        if commits:
            lines.append("| Date | Commit | Message |")
            lines.append("|------|--------|---------|")
            for c in commits[:20]:
                lines.append(f"| {c['date']} | `{c['hash']}` | {c['message']} |")
        else:
            lines.append("No git history found.")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Correlation alerts
    lines.append("## Correlation Alerts")
    lines.append("")
    lines.append("> Runs that failed within 2 days of a plan edit:")
    lines.append("")

    plan_dates = set()
    for commits in plan_history.values():
        for c in commits:
            plan_dates.add(c["date"])

    alerts_found = False
    for r in run_results:
        if r["failed"] > 0:
            for pd in plan_dates:
                try:
                    plan_dt = datetime.strptime(pd, "%Y-%m-%d")
                    run_dt = datetime.strptime(r["date"][:10], "%Y-%m-%d")
                    delta = abs((run_dt - plan_dt).days)
                    if delta <= 2:
                        lines.append(
                            f"- **{r['file']}** failed on {r['date']} — "
                            f"plan edited on {pd} (delta: {delta} day(s))"
                        )
                        alerts_found = True
                except ValueError:
                    pass

    if not alerts_found:
        lines.append("No correlations found — failures did not coincide with recent plan edits.")
    lines.append("")

    # Drift notes from reports
    drift_reports = [r for r in run_results if r["has_drift"]]
    if drift_reports:
        lines.append("---")
        lines.append("")
        lines.append("## Reports with Drift Detected")
        lines.append("")
        for r in drift_reports:
            lines.append(f"### {r['file']} ({r['date']})")
            for note in r["drift_notes"]:
                lines.append(f"- {note}")
            lines.append("")

    return "\n".join(lines)


def main():
    # Get git history for each test plan
    plan_files = sorted(PLANS_DIR.glob("e2e-*.md"))
    plan_history = {}
    for pf in plan_files:
        commits = get_git_log(pf)
        plan_history[pf.name] = commits
        print(f"  {pf.name}: {len(commits)} commits")

    # Parse all test reports
    run_results = []
    for rf in sorted(REPORTS_DIR.rglob("*.md")):
        result = parse_report_results(rf)
        if result:
            run_results.append(result)

    print(f"\n{len(plan_files)} test plans, {len(run_results)} test runs")

    report = generate_report(plan_history, run_results)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"Report saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
