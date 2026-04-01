"""
Stale Test Plan Detector — flags test plans that haven't been run recently.

Usage:
    py reporting/stale-plans.py
    py reporting/stale-plans.py --threshold 14    # custom days threshold (default: 7)

Output: reporting/metrics/stale-plans.md
"""

import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PLANS_DIR = PROJECT_ROOT / "test-plans"
REPORTS_DIR = PROJECT_ROOT / "test-reports"
OUTPUT_FILE = PROJECT_ROOT / "reporting" / "metrics" / "stale-plans.md"

DEFAULT_THRESHOLD_DAYS = 7


def get_plan_metadata(filepath: Path) -> dict:
    """Extract metadata from a test plan."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    meta = {
        "file": filepath.name,
        "path": str(filepath.relative_to(PROJECT_ROOT)),
        "title": "",
        "last_tested": "",
        "status": "",
        "tc_count": 0,
    }

    for line in lines:
        if line.startswith("# "):
            meta["title"] = line.lstrip("# ").strip()
        m = re.search(r"Last tested\s*\|\s*(.+)", line)
        if m:
            meta["last_tested"] = m.group(1).strip()
        m = re.search(r"Status\s*\|\s*(.+)", line)
        if m:
            meta["status"] = m.group(1).strip()

    meta["tc_count"] = len(re.findall(r"^##\s+TC-", content, re.MULTILINE))

    return meta


def find_latest_run(plan_name: str) -> tuple[str, str]:
    """Find the most recent report for a test plan, return (date, filename)."""
    # Map plan name to module directory
    module_map = {
        "e2e-personal-loan-application.md": "personal-loan",
        "e2e-entity-loan-application.md": "entity-loan",
        "e2e-negative-edge-cases.md": "negative-edge-cases",
    }

    module = module_map.get(plan_name, "")
    module_dir = REPORTS_DIR / module

    latest_date = ""
    latest_file = ""

    # Check report files in module dir
    if module_dir.exists():
        for rf in module_dir.glob("*.md"):
            content = rf.read_text(encoding="utf-8")
            for line in content.split("\n")[:10]:
                if "**Date:**" in line:
                    date = line.split("**Date:**")[1].strip()[:10]
                    if date > latest_date:
                        latest_date = date
                        latest_file = rf.name

    # Also check the plan's Reports table
    plan_path = PLANS_DIR / plan_name
    if plan_path.exists():
        content = plan_path.read_text(encoding="utf-8")
        dates = re.findall(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|", content)
        for d in dates:
            if d > latest_date:
                latest_date = d

    return latest_date, latest_file


def generate_report(plans: list[dict], threshold_days: int) -> str:
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%dT%H:%M")
    cutoff = (now - timedelta(days=threshold_days)).strftime("%Y-%m-%d")

    lines = [
        "# Stale Test Plan Detector",
        f"**Generated:** {now_str}",
        f"**Threshold:** {threshold_days} days (stale if last run before {cutoff})",
        "",
        "---",
        "",
    ]

    stale = []
    fresh = []
    never_run = []

    for p in plans:
        if not p["latest_run_date"]:
            never_run.append(p)
        elif p["latest_run_date"] < cutoff:
            p["days_since"] = (now - datetime.strptime(p["latest_run_date"], "%Y-%m-%d")).days
            stale.append(p)
        else:
            p["days_since"] = (now - datetime.strptime(p["latest_run_date"], "%Y-%m-%d")).days
            fresh.append(p)

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Status | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Fresh (run within {threshold_days} days) | {len(fresh)} |")
    lines.append(f"| Stale (not run in {threshold_days}+ days) | **{len(stale)}** |")
    lines.append(f"| Never run | **{len(never_run)}** |")
    lines.append(f"| **Total plans** | **{len(plans)}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Stale plans
    if stale:
        lines.append("## Stale Plans")
        lines.append("")
        lines.append("> These plans haven't been run in over the threshold period.")
        lines.append("")
        lines.append("| Plan | Last Run | Days Ago | TCs | Status |")
        lines.append("|------|----------|----------|-----|--------|")
        for p in sorted(stale, key=lambda x: x["days_since"], reverse=True):
            lines.append(
                f"| {p['file']} | {p['latest_run_date']} | "
                f"**{p['days_since']}** | {p['tc_count']} | {p['status']} |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")

    # Never run
    if never_run:
        lines.append("## Never Run")
        lines.append("")
        lines.append("| Plan | TCs Defined | Plan Status |")
        lines.append("|------|-------------|-------------|")
        for p in never_run:
            lines.append(f"| {p['file']} | {p['tc_count']} | {p['status'] or '—'} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Fresh plans
    if fresh:
        lines.append("## Fresh Plans")
        lines.append("")
        lines.append("| Plan | Last Run | Days Ago | TCs |")
        lines.append("|------|----------|----------|-----|")
        for p in sorted(fresh, key=lambda x: x["days_since"]):
            lines.append(
                f"| {p['file']} | {p['latest_run_date']} | "
                f"{p['days_since']} | {p['tc_count']} |"
            )
        lines.append("")

    # Recommendations
    lines.append("---")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    if stale:
        lines.append(f"- **{len(stale)} stale plan(s)** should be re-run to confirm they still pass")
        for p in stale:
            lines.append(f"  - `{p['file']}` — last run {p['days_since']} days ago")
    if never_run:
        lines.append(f"- **{len(never_run)} plan(s) never executed** — schedule an initial run")
        for p in never_run:
            lines.append(f"  - `{p['file']}` — {p['tc_count']} TCs defined but never tested")
    if not stale and not never_run:
        lines.append("All test plans are up to date.")
    lines.append("")

    return "\n".join(lines)


def main():
    threshold = DEFAULT_THRESHOLD_DAYS
    if "--threshold" in sys.argv:
        idx = sys.argv.index("--threshold")
        if idx + 1 < len(sys.argv):
            threshold = int(sys.argv[idx + 1])

    plan_files = sorted(PLANS_DIR.glob("e2e-*.md"))
    plans = []

    for pf in plan_files:
        meta = get_plan_metadata(pf)
        latest_date, latest_file = find_latest_run(pf.name)
        meta["latest_run_date"] = latest_date
        meta["latest_run_file"] = latest_file

        status = f"last run: {latest_date}" if latest_date else "NEVER RUN"
        print(f"  {pf.name}: {meta['tc_count']} TCs, {status}")
        plans.append(meta)

    report = generate_report(plans, threshold)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    print(f"\n{len(plans)} plans checked (threshold: {threshold} days)")
    print(f"Report saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
