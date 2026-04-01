# Drift History Log
**Generated:** 2026-04-01T13:41

> Correlates test plan changes (git history) with test run results to identify
> whether plan edits coincide with test failures or regressions.

---

## Timeline

| Date | Event | Source | Detail |
|------|-------|--------|--------|
| 2026-03-17 | PLAN EDIT | e2e-entity-loan-application.md | Initial commit: E2E Playwright tests for LandBank CRM `8e8965cb` |
| 2026-03-17 | PLAN EDIT | e2e-personal-loan-application.md | Initial commit: E2E Playwright tests for LandBank CRM `8e8965cb` |
| 2026-03-17 | TEST RUN | entity-loan | PASS — opportunity-entity-edit-2026-03-17.md |
| 2026-03-17 | TEST RUN | personal-loan | PASS — e2e-personal-loan-run2-2026-03-17.md |
| 2026-03-17 | TEST RUN | personal-loan | PASS — workflow-end-to-end-2026-03-17.md |
| 2026-03-18 | PLAN EDIT | e2e-entity-loan-application.md | Add E2E Entity (Close Corporation) loan test plan, report, and CI support `165f585b` |
| 2026-03-18 | PLAN EDIT | e2e-negative-edge-cases.md | Add negative/edge case test plan, upgrade dashboard with assertions `e286676a` |
| 2026-03-18 | TEST RUN | entity-loan | PASS — e2e-entity-loan-application-ci-23264586931-2026-03-18T20-48.md |
| 2026-03-18 | TEST RUN | entity-loan | PASS — e2e-entity-loan-run1-2026-03-18.md |
| 2026-03-18 | TEST RUN | personal-loan | PASS — e2e-personal-loan-run2-2026-03-18.md |
| 2026-03-18 | TEST RUN | personal-loan | PASS — e2e-personal-loan-run3-2026-03-18.md |
| 2026-03-19 | PLAN EDIT | e2e-entity-loan-application.md | Assert spouse appears in verification when married in community of property `94e9c337` |
| 2026-03-19 | PLAN EDIT | e2e-entity-loan-application.md | Update entity test plan: resolution flow, testmail for all directors `61b8a6d2` |
| 2026-03-19 | PLAN EDIT | e2e-entity-loan-application.md | Rewrite TC-06: per-individual verification with full assertions `774e30dd` |
| 2026-03-19 | PLAN EDIT | e2e-entity-loan-application.md | Add consent flow (TC-05c) with testmail.app for email/OTP verification `8c04c265` |
| 2026-03-19 | PLAN EDIT | e2e-personal-loan-application.md | Assert spouse appears in verification when married in community of property `94e9c337` |
| 2026-03-19 | PLAN EDIT | e2e-personal-loan-application.md | Rewrite TC-06: per-individual verification with full assertions `774e30dd` |
| 2026-03-19 | PLAN EDIT | e2e-personal-loan-application.md | Add consent flow (TC-05c) with testmail.app for email/OTP verification `8c04c265` |
| 2026-03-19 | TEST RUN | entity-loan | PASS — entity-loan-2026-03-19T15-18.md |
| 2026-03-19 | TEST RUN | personal-loan | PASS — e2e-personal-loan-application-ci-23276371190-2026-03-19T02-22.md |
| 2026-03-19 | TEST RUN | personal-loan | PASS — personal-loan-2026-03-19T15-18.md |
| 2026-03-24 | PLAN EDIT | e2e-entity-loan-application.md | Add report links to test plans, sequential CI jobs, remove Auto Verify `4e05d25f` |
| 2026-03-24 | PLAN EDIT | e2e-negative-edge-cases.md | Add report links to test plans, sequential CI jobs, remove Auto Verify `4e05d25f` |
| 2026-03-24 | PLAN EDIT | e2e-personal-loan-application.md | Add report links to test plans, sequential CI jobs, remove Auto Verify `4e05d25f` |
| 2026-04-01 | PLAN EDIT | e2e-personal-loan-application.md | Simplify CI to entity-loan only, update templates with anti-script guardrails, remove Auto Verify `8d607bac` |

---

## Test Plan Change History

### e2e-entity-loan-application.md
**Total edits:** 7

| Date | Commit | Message |
|------|--------|---------|
| 2026-03-24 | `4e05d25f` | Add report links to test plans, sequential CI jobs, remove Auto Verify |
| 2026-03-19 | `94e9c337` | Assert spouse appears in verification when married in community of property |
| 2026-03-19 | `61b8a6d2` | Update entity test plan: resolution flow, testmail for all directors |
| 2026-03-19 | `774e30dd` | Rewrite TC-06: per-individual verification with full assertions |
| 2026-03-19 | `8c04c265` | Add consent flow (TC-05c) with testmail.app for email/OTP verification |
| 2026-03-18 | `165f585b` | Add E2E Entity (Close Corporation) loan test plan, report, and CI support |
| 2026-03-17 | `8e8965cb` | Initial commit: E2E Playwright tests for LandBank CRM |

### e2e-negative-edge-cases.md
**Total edits:** 2

| Date | Commit | Message |
|------|--------|---------|
| 2026-03-24 | `4e05d25f` | Add report links to test plans, sequential CI jobs, remove Auto Verify |
| 2026-03-18 | `e286676a` | Add negative/edge case test plan, upgrade dashboard with assertions |

### e2e-personal-loan-application.md
**Total edits:** 6

| Date | Commit | Message |
|------|--------|---------|
| 2026-04-01 | `8d607bac` | Simplify CI to entity-loan only, update templates with anti-script guardrails, remove Auto Verify |
| 2026-03-24 | `4e05d25f` | Add report links to test plans, sequential CI jobs, remove Auto Verify |
| 2026-03-19 | `94e9c337` | Assert spouse appears in verification when married in community of property |
| 2026-03-19 | `774e30dd` | Rewrite TC-06: per-individual verification with full assertions |
| 2026-03-19 | `8c04c265` | Add consent flow (TC-05c) with testmail.app for email/OTP verification |
| 2026-03-17 | `8e8965cb` | Initial commit: E2E Playwright tests for LandBank CRM |

---

## Correlation Alerts

> Runs that failed within 2 days of a plan edit:

No correlations found — failures did not coincide with recent plan edits.
