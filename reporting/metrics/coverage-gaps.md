# Coverage Gap Report
**Generated:** 2026-04-01T13:41

---

## Test Plan Coverage

| Plan | TCs Defined | TCs Executed (ever) | Coverage |
|------|-------------|---------------------|----------|
| e2e-entity-loan-application.md | 0 | 0 | 0% |
| e2e-negative-edge-cases.md | 0 | 0 | 0% |
| e2e-personal-loan-application.md | 0 | 0 | 0% |

---

## Feature Coverage Matrix

> Checks each app feature against test plan mentions.

| Feature | Has Test Plan | Has Been Run | Status |
|---------|--------------|-------------|--------|
| Lead Creation | **No** | Yes | **GAP** |
| Pre-Screening | Yes | Yes | Covered |
| Opportunity Setup - Client Info | **No** | Yes | **GAP** |
| Opportunity Setup - Loan Info | Yes | Yes | Covered |
| Opportunity Setup - Farms | Yes | Yes | Covered |
| Entity - Directors | Yes | Yes | Covered |
| Entity - Signatories | **No** | Yes | **GAP** |
| Initiate Loan Application | Yes | Yes | Covered |
| Consent Flow - Personal | Yes | Yes | Covered |
| Resolution Flow - Entity | Yes | No | Planned, not run |
| Verification Review | Yes | Yes | Covered |
| Onboarding Checklist | Yes | Yes | Covered |
| Negative - Pre-Screening Failures | Yes | Yes | Covered |
| Negative - Loan Validation | Yes | Yes | Covered |
| Negative - Field Validation | Yes | Yes | Covered |
| Negative - Workflow Edge Cases | Yes | Yes | Covered |

---

## Test Cases Never Executed

All defined test cases have been executed at least once.

---

## Suggested New Test Areas

- Multi-browser testing (Chrome, Firefox, Edge)
- Mobile responsive testing (viewport sizes)
- Concurrent user testing (two RMs editing same opportunity)
- Session timeout handling
- File upload scenarios (documents, oversized files)
- Pagination and sorting on table views
- Search/filter functionality on Leads and Opportunities tables
- Permission-based access (admin vs RM vs read-only)
- Data export/download functionality
- Audit trail / activity log verification
