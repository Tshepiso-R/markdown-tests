"""
Cost Report — tracks verification API costs from SA ID usage across test runs.

Tracks:
- ID verification calls (per unique SA ID per run)
- KYC verification calls
- Testmail.app API calls (email retrieval)
- OTP requests
- Estimated costs per run and cumulative

Usage:
    py reporting/cost-report.py

Output: reporting/metrics/cost-report.md
"""

import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "test-reports"
OUTPUT_FILE = PROJECT_ROOT / "reporting" / "metrics" / "cost-report.md"

# Approved IDs from RULES.md — reuse is free after first verification
APPROVED_IDS = {
    "7708206169188": "Ian Houvet",
    "7304190225085": "Chamaine Houvet",
    "6311115651080": "Xolile Ndlangana",
}

# Cost estimates (ZAR) — adjust these to match your actual vendor pricing
COSTS = {
    "id_verification": 15.00,       # Per ID verification API call
    "kyc_verification": 12.00,      # Per KYC lookup
    "otp_sms": 0.50,                # Per OTP SMS sent
    "testmail_api_call": 0.00,      # Testmail.app — free tier
    "consent_email": 0.00,          # System-generated, no direct cost
}


def parse_report_costs(filepath: Path) -> dict | None:
    """Extract cost-relevant actions from a report."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    meta = {
        "file": filepath.name,
        "module": filepath.parent.name,
        "date": "",
        "ids_used": set(),
        "unapproved_ids": set(),
        "id_verifications": 0,
        "kyc_verifications": 0,
        "otp_requests": 0,
        "testmail_calls": 0,
        "consent_emails": 0,
    }

    for line in lines[:10]:
        if "**Date:**" in line:
            meta["date"] = line.split("**Date:**")[1].strip()[:10]

    # Find all SA ID numbers mentioned (13 digits)
    id_matches = re.findall(r"\b(\d{13})\b", content)
    for id_num in id_matches:
        # Basic SA ID validation (starts with valid date-like prefix)
        if id_num[:2].isdigit() and int(id_num[:2]) <= 99:
            meta["ids_used"].add(id_num)
            if id_num not in APPROVED_IDS:
                meta["unapproved_ids"].add(id_num)

    # Count verification events
    meta["id_verifications"] = len(re.findall(
        r"ID Verification.*Completed|ID Verification.*Status|Submitted:.*\d{13}",
        content, re.IGNORECASE
    ))

    meta["kyc_verifications"] = len(re.findall(
        r"KYC Verification.*Completed|KYC Verification.*Status|KYC First Name",
        content, re.IGNORECASE
    ))

    # Count OTP requests
    meta["otp_requests"] = len(re.findall(
        r"Request OTP|OTP.*sent|One-Time-Pin|Submit OTP",
        content, re.IGNORECASE
    ))
    # Deduplicate: "Request OTP" and "OTP sent" are same event
    meta["otp_requests"] = max(
        len(re.findall(r"Request OTP|Clicked.*Request OTP", content, re.IGNORECASE)),
        len(re.findall(r"OTP email received|OTP:?\s*\d{6}", content, re.IGNORECASE)),
    )

    # Count testmail.app API calls
    meta["testmail_calls"] = len(re.findall(
        r"testmail\.app API|api\.testmail\.app",
        content, re.IGNORECASE
    ))

    # Count consent emails
    meta["consent_emails"] = len(re.findall(
        r"consent email|resolution email|Action Required.*Consent|Action Required.*Resolution",
        content, re.IGNORECASE
    ))

    if not meta["date"]:
        return None

    return meta


def generate_report(runs: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")

    lines = [
        "# Cost Report — Verification & API Usage",
        f"**Generated:** {now}",
        "",
        "---",
        "",
    ]

    # Totals
    total_id = sum(r["id_verifications"] for r in runs)
    total_kyc = sum(r["kyc_verifications"] for r in runs)
    total_otp = sum(r["otp_requests"] for r in runs)
    total_testmail = sum(r["testmail_calls"] for r in runs)
    total_consent = sum(r["consent_emails"] for r in runs)

    all_ids = set()
    all_unapproved = set()
    for r in runs:
        all_ids.update(r["ids_used"])
        all_unapproved.update(r["unapproved_ids"])

    total_cost = (
        total_id * COSTS["id_verification"]
        + total_kyc * COSTS["kyc_verification"]
        + total_otp * COSTS["otp_sms"]
        + total_testmail * COSTS["testmail_api_call"]
    )

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Count | Unit Cost (ZAR) | Total (ZAR) |")
    lines.append(f"|--------|-------|-----------------|-------------|")
    lines.append(f"| ID Verifications | {total_id} | R{COSTS['id_verification']:.2f} | R{total_id * COSTS['id_verification']:.2f} |")
    lines.append(f"| KYC Verifications | {total_kyc} | R{COSTS['kyc_verification']:.2f} | R{total_kyc * COSTS['kyc_verification']:.2f} |")
    lines.append(f"| OTP SMS | {total_otp} | R{COSTS['otp_sms']:.2f} | R{total_otp * COSTS['otp_sms']:.2f} |")
    lines.append(f"| Testmail.app API calls | {total_testmail} | Free | R0.00 |")
    lines.append(f"| Consent/Resolution Emails | {total_consent} | System | R0.00 |")
    lines.append(f"| **Total Estimated Cost** | | | **R{total_cost:.2f}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ID usage
    lines.append("## SA ID Numbers Used")
    lines.append("")
    lines.append("| ID Number | Person | Status | Times Seen |")
    lines.append("|-----------|--------|--------|------------|")

    id_counts = Counter()
    for r in runs:
        for id_num in r["ids_used"]:
            id_counts[id_num] += 1

    for id_num, count in id_counts.most_common():
        person = APPROVED_IDS.get(id_num, "**UNKNOWN**")
        status = "Approved" if id_num in APPROVED_IDS else "**UNAPPROVED**"
        lines.append(f"| {id_num} | {person} | {status} | {count} |")

    lines.append("")

    if all_unapproved:
        lines.append(f"> **WARNING:** {len(all_unapproved)} unapproved ID(s) detected! Each new ID triggers a paid verification.")
        lines.append(">")
        for uid in sorted(all_unapproved):
            lines.append(f"> - `{uid}`")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Cost per run
    lines.append("## Cost Per Run")
    lines.append("")
    lines.append("| Date | Module | Report | ID Verif | KYC | OTPs | Est. Cost |")
    lines.append("|------|--------|--------|----------|-----|------|-----------|")

    for r in sorted(runs, key=lambda x: x["date"], reverse=True):
        run_cost = (
            r["id_verifications"] * COSTS["id_verification"]
            + r["kyc_verifications"] * COSTS["kyc_verification"]
            + r["otp_requests"] * COSTS["otp_sms"]
        )
        lines.append(
            f"| {r['date']} | {r['module']} | {r['file']} | "
            f"{r['id_verifications']} | {r['kyc_verifications']} | "
            f"{r['otp_requests']} | R{run_cost:.2f} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Cost trend
    monthly = defaultdict(float)
    for r in runs:
        month = r["date"][:7]  # YYYY-MM
        run_cost = (
            r["id_verifications"] * COSTS["id_verification"]
            + r["kyc_verifications"] * COSTS["kyc_verification"]
            + r["otp_requests"] * COSTS["otp_sms"]
        )
        monthly[month] += run_cost

    if monthly:
        lines.append("## Monthly Cost Trend")
        lines.append("")
        lines.append("| Month | Estimated Cost (ZAR) | Runs |")
        lines.append("|-------|---------------------|------|")
        monthly_runs = Counter()
        for r in runs:
            monthly_runs[r["date"][:7]] += 1
        for month in sorted(monthly.keys()):
            lines.append(f"| {month} | R{monthly[month]:.2f} | {monthly_runs[month]} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Savings tips
    lines.append("## Cost Optimization")
    lines.append("")
    lines.append(f"- **Approved IDs reused:** {len(all_ids & set(APPROVED_IDS.keys()))} of {len(APPROVED_IDS)} — reuse saves ~R{COSTS['id_verification'] + COSTS['kyc_verification']:.2f} per new ID")

    if all_unapproved:
        wasted = len(all_unapproved) * (COSTS["id_verification"] + COSTS["kyc_verification"])
        lines.append(f"- **Unapproved ID cost:** ~R{wasted:.2f} wasted on {len(all_unapproved)} unrecognized ID(s)")

    lines.append(f"- **Total runs:** {len(runs)} across {len(monthly)} month(s)")
    lines.append(f"- **Avg cost per run:** R{total_cost / len(runs):.2f}" if runs else "")
    lines.append("")

    # Pricing note
    lines.append("---")
    lines.append("")
    lines.append("## Pricing Reference")
    lines.append("")
    lines.append("> Costs are estimates. Update `COSTS` dict in `reporting/cost-report.py` to match actual vendor pricing.")
    lines.append("")
    lines.append("| Service | Unit Cost |")
    lines.append("|---------|-----------|")
    for service, cost in COSTS.items():
        lines.append(f"| {service.replace('_', ' ').title()} | R{cost:.2f} |")
    lines.append("")

    return "\n".join(lines)


def main():
    report_files = sorted(REPORTS_DIR.rglob("*.md"))
    runs = []

    for f in report_files:
        result = parse_report_costs(f)
        if result:
            ids = ", ".join(sorted(result["ids_used"]))[:40]
            print(f"  {result['file']}: {result['id_verifications']} ID, {result['kyc_verifications']} KYC, {result['otp_requests']} OTP")
            runs.append(result)

    report = generate_report(runs)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    total_cost = sum(
        r["id_verifications"] * COSTS["id_verification"]
        + r["kyc_verifications"] * COSTS["kyc_verification"]
        + r["otp_requests"] * COSTS["otp_sms"]
        for r in runs
    )
    print(f"\n{len(runs)} runs analyzed")
    print(f"Estimated total cost: R{total_cost:.2f}")
    print(f"Report saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
