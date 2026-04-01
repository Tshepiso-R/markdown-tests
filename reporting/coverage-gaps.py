"""
Coverage Gap Detector — compares test plans against app routes/features to find untested areas.

Usage:
    py reporting/coverage-gaps.py

Output: reporting/metrics/coverage-gaps.md
"""

import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PLANS_DIR = PROJECT_ROOT / "test-plans"
REPORTS_DIR = PROJECT_ROOT / "test-reports"
OUTPUT_FILE = PROJECT_ROOT / "reporting" / "metrics" / "coverage-gaps.md"

# Known application features/routes to check coverage against
# Derived from the test plans and app structure
APP_FEATURES = {
    "Lead Creation": {
        "routes": ["LBLead-table", "LBLead-details"],
        "actions": ["Create Individual Lead", "Create Entity Lead"],
    },
    "Pre-Screening": {
        "routes": ["LBLead-details"],
        "actions": ["Initiate Pre-Screening", "Answer screening questions", "Submit screening"],
    },
    "Opportunity Setup - Client Info": {
        "routes": ["LBOpportunity-details"],
        "actions": ["Edit client info", "Set ID number", "Set address", "Set marital status"],
    },
    "Opportunity Setup - Loan Info": {
        "routes": ["LBOpportunity-details"],
        "actions": ["Select product", "Set amount", "Add loan purpose", "Set income source"],
    },
    "Opportunity Setup - Farms": {
        "routes": ["LBOpportunity-details"],
        "actions": ["Add farm", "Edit farm details"],
    },
    "Entity - Directors": {
        "routes": ["LBOpportunity-details"],
        "actions": ["Add director", "Set director ID", "Set marital status", "Add spouse"],
    },
    "Entity - Signatories": {
        "routes": ["LBOpportunity-details"],
        "actions": ["Add signatory", "Set signatory details"],
    },
    "Initiate Loan Application": {
        "routes": ["LBOpportunity-details"],
        "actions": ["Click Initiate", "Validate required fields", "Status changes to Consent/Resolution Pending"],
    },
    "Consent Flow - Personal": {
        "routes": ["individual-application-consent"],
        "actions": ["Receive consent email", "Open consent URL", "Request OTP", "Submit OTP", "Sign consent"],
    },
    "Resolution Flow - Entity": {
        "routes": ["resolution-consent"],
        "actions": ["Director receives resolution email", "Sign resolution", "All directors sign"],
    },
    "Verification Review": {
        "routes": ["workflow-action"],
        "actions": ["Review ID verification", "Review KYC", "Approve/Reject", "Finalise outcomes"],
    },
    "Onboarding Checklist": {
        "routes": ["workflow-action"],
        "actions": ["Fill checklist items", "Submit checklist", "Workflow completes"],
    },
    "Negative - Pre-Screening Failures": {
        "routes": ["LBLead-details"],
        "actions": ["Disqualifying answers", "Missing checkbox", "Partial answers"],
    },
    "Negative - Loan Validation": {
        "routes": ["LBOpportunity-details"],
        "actions": ["Missing amount", "Missing product", "Missing owner", "Zero amount"],
    },
    "Negative - Field Validation": {
        "routes": ["LBLead-table", "LBOpportunity-details"],
        "actions": ["Invalid ID number", "Duplicate ID", "Empty mandatory fields", "Invalid email"],
    },
    "Negative - Workflow Edge Cases": {
        "routes": ["workflow-action"],
        "actions": ["Edit after workflow start", "Partial checklist", "Navigation persistence"],
    },
}


def parse_plan_coverage(filepath: Path) -> dict:
    """Extract what features/TCs a test plan covers."""
    content = filepath.read_text(encoding="utf-8")

    coverage = {
        "file": filepath.name,
        "tc_ids": [],
        "tc_names": [],
        "routes_mentioned": set(),
        "actions_mentioned": set(),
    }

    # Extract TC IDs and names
    for m in re.finditer(r"^##\s+(TC-\S+):\s*(.+)$", content, re.MULTILINE):
        coverage["tc_ids"].append(m.group(1))
        coverage["tc_names"].append(m.group(2).strip())

    # Extract mentioned routes
    for route in re.findall(r"(LBLead-table|LBLead-details|LBOpportunity-details|LBOpportunity-table|workflow-action|individual-application-consent|resolution-consent)", content):
        coverage["routes_mentioned"].add(route)

    # Extract action keywords
    content_lower = content.lower()
    action_keywords = [
        "create lead", "pre-screening", "edit client", "loan info", "farms",
        "director", "signatory", "initiate loan", "consent", "resolution",
        "verification", "onboarding", "checklist", "negative", "edge case",
        "invalid", "duplicate", "missing", "zero amount",
    ]
    for kw in action_keywords:
        if kw in content_lower:
            coverage["actions_mentioned"].add(kw)

    return coverage


def parse_report_coverage(filepath: Path) -> set:
    """Extract TC IDs that were actually executed in a report."""
    content = filepath.read_text(encoding="utf-8")
    executed = set()
    for m in re.finditer(r"^## (TC-\S+)", content, re.MULTILINE):
        executed.add(m.group(1))
    return executed


def generate_report(plan_coverages: list[dict], executed_tcs: dict, last_run_dates: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")

    lines = [
        "# Coverage Gap Report",
        f"**Generated:** {now}",
        "",
        "---",
        "",
    ]

    # Summary per plan
    all_planned_tcs = set()
    all_executed_tcs = set()

    lines.append("## Test Plan Coverage")
    lines.append("")
    lines.append("| Plan | TCs Defined | TCs Executed (ever) | Coverage |")
    lines.append("|------|-------------|---------------------|----------|")

    for pc in plan_coverages:
        plan_key = pc["file"].replace("e2e-", "").replace(".md", "")
        planned = set(pc["tc_ids"])
        executed = executed_tcs.get(plan_key, set())
        all_planned_tcs.update(planned)
        all_executed_tcs.update(executed)

        covered = len(planned & executed)
        total = len(planned)
        pct = round(covered / total * 100, 1) if total else 0
        lines.append(f"| {pc['file']} | {total} | {covered} | {pct}% |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Feature coverage matrix
    lines.append("## Feature Coverage Matrix")
    lines.append("")
    lines.append("> Checks each app feature against test plan mentions.")
    lines.append("")
    lines.append("| Feature | Has Test Plan | Has Been Run | Status |")
    lines.append("|---------|--------------|-------------|--------|")

    all_actions = set()
    for pc in plan_coverages:
        all_actions.update(pc["actions_mentioned"])

    for feature, details in APP_FEATURES.items():
        # Check if any plan covers this feature
        feature_kw = feature.lower()
        has_plan = any(
            any(kw in feature_kw or feature_kw in kw for kw in pc["actions_mentioned"])
            for pc in plan_coverages
        )

        # Check if routes are in any report
        has_run = False
        for rf in sorted(REPORTS_DIR.rglob("*.md")):
            content = rf.read_text(encoding="utf-8")
            for route in details["routes"]:
                if route in content:
                    has_run = True
                    break
            if has_run:
                break

        if has_plan and has_run:
            status = "Covered"
        elif has_plan:
            status = "Planned, not run"
        else:
            status = "**GAP**"

        lines.append(f"| {feature} | {'Yes' if has_plan else '**No**'} | {'Yes' if has_run else 'No'} | {status} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Unexecuted TCs
    lines.append("## Test Cases Never Executed")
    lines.append("")
    never_run = []
    for pc in plan_coverages:
        plan_key = pc["file"].replace("e2e-", "").replace(".md", "")
        executed = executed_tcs.get(plan_key, set())
        for i, tc_id in enumerate(pc["tc_ids"]):
            if tc_id not in executed:
                never_run.append({
                    "plan": pc["file"],
                    "tc": tc_id,
                    "name": pc["tc_names"][i] if i < len(pc["tc_names"]) else "",
                })

    if never_run:
        lines.append("| Plan | TC | Name |")
        lines.append("|------|----|------|")
        for nr in never_run:
            lines.append(f"| {nr['plan']} | {nr['tc']} | {nr['name']} |")
    else:
        lines.append("All defined test cases have been executed at least once.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Suggested new test areas
    lines.append("## Suggested New Test Areas")
    lines.append("")
    suggestions = [
        "Multi-browser testing (Chrome, Firefox, Edge)",
        "Mobile responsive testing (viewport sizes)",
        "Concurrent user testing (two RMs editing same opportunity)",
        "Session timeout handling",
        "File upload scenarios (documents, oversized files)",
        "Pagination and sorting on table views",
        "Search/filter functionality on Leads and Opportunities tables",
        "Permission-based access (admin vs RM vs read-only)",
        "Data export/download functionality",
        "Audit trail / activity log verification",
    ]
    for s in suggestions:
        lines.append(f"- {s}")
    lines.append("")

    return "\n".join(lines)


def main():
    # Parse all test plans
    plan_files = sorted(PLANS_DIR.glob("e2e-*.md"))
    plan_coverages = []
    for pf in plan_files:
        pc = parse_plan_coverage(pf)
        print(f"  {pf.name}: {len(pc['tc_ids'])} TCs defined")
        plan_coverages.append(pc)

    # Parse all reports to find executed TCs by module
    executed_tcs = defaultdict(set)
    last_run_dates = {}
    for rf in sorted(REPORTS_DIR.rglob("*.md")):
        module = rf.parent.name
        tcs = parse_report_coverage(rf)
        # Map module to plan key
        plan_key = module.replace("-", "-")  # e.g. personal-loan
        # Try to match to plan names
        for pc in plan_coverages:
            pk = pc["file"].replace("e2e-", "").replace(".md", "").replace("-application", "")
            if pk.replace("-", "") in module.replace("-", ""):
                executed_tcs[pc["file"].replace("e2e-", "").replace(".md", "")].update(tcs)

        # Track last run date
        content = rf.read_text(encoding="utf-8")
        for line in content.split("\n")[:10]:
            if "**Date:**" in line:
                date = line.split("**Date:**")[1].strip()[:10]
                if module not in last_run_dates or date > last_run_dates[module]:
                    last_run_dates[module] = date

    report = generate_report(plan_coverages, executed_tcs, last_run_dates)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    print(f"\n{len(plan_coverages)} plans, {sum(len(v) for v in executed_tcs.values())} unique TC executions tracked")
    print(f"Report saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
