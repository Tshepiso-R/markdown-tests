# Cost Report — Verification & API Usage
**Generated:** 2026-04-01T13:41

---

## Summary

| Metric | Count | Unit Cost (ZAR) | Total (ZAR) |
|--------|-------|-----------------|-------------|
| ID Verifications | 9 | R15.00 | R135.00 |
| KYC Verifications | 5 | R12.00 | R60.00 |
| OTP SMS | 3 | R0.50 | R1.50 |
| Testmail.app API calls | 4 | Free | R0.00 |
| Consent/Resolution Emails | 6 | System | R0.00 |
| **Total Estimated Cost** | | | **R196.50** |

---

## SA ID Numbers Used

| ID Number | Person | Status | Times Seen |
|-----------|--------|--------|------------|
| 7708206169188 | Ian Houvet | Approved | 12 |
| 6311115651080 | Xolile Ndlangana | Approved | 4 |
| 7304190225085 | Chamaine Houvet | Approved | 4 |

---

## Cost Per Run

| Date | Module | Report | ID Verif | KYC | OTPs | Est. Cost |
|------|--------|--------|----------|-----|------|-----------|
| 2026-03-19 | entity-loan | entity-loan-2026-03-19T15-18.md | 0 | 0 | 1 | R0.50 |
| 2026-03-19 | personal-loan | e2e-personal-loan-application-ci-23276371190-2026-03-19T02-22.md | 1 | 0 | 0 | R15.00 |
| 2026-03-19 | personal-loan | personal-loan-2026-03-19T15-18.md | 4 | 2 | 2 | R85.00 |
| 2026-03-18 | entity-loan | e2e-entity-loan-application-ci-23264586931-2026-03-18T20-48.md | 0 | 0 | 0 | R0.00 |
| 2026-03-18 | entity-loan | e2e-entity-loan-run1-2026-03-18.md | 0 | 0 | 0 | R0.00 |
| 2026-03-18 | negative-edge-cases | e2e-negative-edge-cases-ci-23266964791-2026-03-18T21-52.md | 0 | 0 | 0 | R0.00 |
| 2026-03-18 | personal-loan | e2e-personal-loan-application-ci-23260437980-2026-03-18T18-42.md | 2 | 3 | 0 | R66.00 |
| 2026-03-18 | personal-loan | e2e-personal-loan-run2-2026-03-18.md | 2 | 0 | 0 | R30.00 |
| 2026-03-18 | personal-loan | e2e-personal-loan-run3-2026-03-18.md | 0 | 0 | 0 | R0.00 |
| 2026-03-17 | entity-loan | opportunity-entity-edit-2026-03-17.md | 0 | 0 | 0 | R0.00 |
| 2026-03-17 | personal-loan | e2e-personal-loan-run2-2026-03-17.md | 0 | 0 | 0 | R0.00 |
| 2026-03-17 | personal-loan | workflow-end-to-end-2026-03-17.md | 0 | 0 | 0 | R0.00 |

---

## Monthly Cost Trend

| Month | Estimated Cost (ZAR) | Runs |
|-------|---------------------|------|
| 2026-03 | R196.50 | 12 |

---

## Cost Optimization

- **Approved IDs reused:** 3 of 3 — reuse saves ~R27.00 per new ID
- **Total runs:** 12 across 1 month(s)
- **Avg cost per run:** R16.38

---

## Pricing Reference

> Costs are estimates. Update `COSTS` dict in `reporting/cost-report.py` to match actual vendor pricing.

| Service | Unit Cost |
|---------|-----------|
| Id Verification | R15.00 |
| Kyc Verification | R12.00 |
| Otp Sms | R0.50 |
| Testmail Api Call | R0.00 |
| Consent Email | R0.00 |
