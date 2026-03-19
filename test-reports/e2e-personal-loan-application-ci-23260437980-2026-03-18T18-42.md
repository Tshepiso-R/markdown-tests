# Test Report — E2E Personal Loan Application
**CI Run ID:** 23260437980
**Date:** 2026-03-18
**Time:** 18:42 UTC+2
**Environment:** https://landbankcrm-adminportal-qa.shesha.app
**Lead Name:** AutoCI23260437980 Houvet
**Executed By:** Claude (automated CI run)
**Report Path:** `test-reports/e2e-personal-loan-application-ci-23260437980-2026-03-18T18-42.md`
**Screenshots:** `test-reports/screenshots/e2e-personal-loan-application-ci-23260437980/`

---

## Summary

| # | Test Case | Result |
|---|-----------|--------|
| TC-01 | Create Individual Lead | ✅ PASS |
| TC-02 | Initiate Pre-Screening | ✅ PASS |
| TC-03 | Edit Client Info | ✅ PASS |
| TC-04 | Fill Loan Info | ✅ PASS |
| TC-05a | Negative: Initiate with Amount = 0 | ✅ PASS |
| TC-05b | Negative: Initiate with no Product | ✅ PASS |
| TC-05 | Initiate Loan Application (happy path) | ✅ PASS |
| TC-06 | Review and Finalise Verification Outcomes | ✅ PASS |
| TC-07 | Fill and Submit Onboarding Checklist | ✅ PASS |

**Total:** 9/9 PASS — 0 FAIL — 0 SKIP

---

## Key IDs (this run)

| Entity | ID |
|--------|----|
| Lead | 93ace498-c487-4406-9352-b5affd44829a |
| Opportunity | 46a5e90f-9f11-4af5-a2d0-959c14e2eeef |
| Account | 129d6591-a8b2-4366-a9a9-028bd69b89bb |
| Workflow Ref | LA2026/0943 |

---

## TC-01: Create Individual Lead

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBLead-table

### Steps Followed
1. Navigated to Leads table
2. Clicked "+ New Lead" button
3. Selected Individual type
4. Filled form: First Name = AutoCI23260437980, Last Name = Houvet, ID = 7708206169188, Email = promise.raganya@boxfusion.io, Mobile = 0712345678
5. Saved the lead

### Assertions
- [x] Lead created with name "AutoCI23260437980 Houvet"
- [x] Lead visible in the table
- [x] Lead ID = 7708206169188

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Leads table](screenshots/e2e-personal-loan-application-ci-23260437980/tc01-leads-table.png) | Leads table before creation |
| ![Lead form filled](screenshots/e2e-personal-loan-application-ci-23260437980/tc01-lead-form-filled.png) | Lead form filled |
| ![Lead created](screenshots/e2e-personal-loan-application-ci-23260437980/tc01-lead-created.png) | Lead created and visible |

### Input vs Output
| Field | Input | Output |
|-------|-------|--------|
| First Name | AutoCI23260437980 | AutoCI23260437980 |
| Last Name | Houvet | Houvet |
| ID Number | 7708206169188 | 7708206169188 |
| Email | promise.raganya@boxfusion.io | promise.raganya@boxfusion.io |
| Mobile | 0712345678 | 0712345678 |

---

## TC-02: Initiate Pre-Screening

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBLead-details?id=93ace498-c487-4406-9352-b5affd44829a

### Steps Followed
1. Opened lead detail page
2. Clicked "Initiate Pre-Screening" button
3. Answered all 7 pre-screening questions (Yes/Yes/Yes/No/No/Yes/Yes)
4. Checked confirmation checkbox
5. Clicked Submit

### Assertions
- [x] Pre-screening form loaded
- [x] All 7 questions answered
- [x] Pre-screening passed (green status)
- [x] Lead status updated to "Pre-Screening Passed"

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Lead detail](screenshots/e2e-personal-loan-application-ci-23260437980/tc02-lead-detail.png) | Lead detail page |
| ![Pre-screening filled](screenshots/e2e-personal-loan-application-ci-23260437980/tc02-prescreening-filled.png) | Pre-screening form answered |
| ![Pre-screening passed](screenshots/e2e-personal-loan-application-ci-23260437980/tc02-prescreening-passed.png) | Pre-screening passed |

### Input vs Output
| Question | Answer | Outcome |
|----------|--------|---------|
| Q1 | Yes | — |
| Q2 | Yes | — |
| Q3 | Yes | — |
| Q4 | No | — |
| Q5 | No | — |
| Q6 | Yes | — |
| Q7 | Yes | — |
| Overall | — | PASSED |

---

## TC-03: Edit Client Info (Opportunity Setup)

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-details?id=46a5e90f-9f11-4af5-a2d0-959c14e2eeef

### Steps Followed
1. Navigated to Opportunity detail (created from lead during pre-screening)
2. Clicked Edit → Client Info tab
3. Filled: Client ID = 7708206169188, Title = Mr, Name = Ian, Surname = Houvet
4. Set email, mobile, preferred communication = Email
5. Set Country of Residence = South Africa, Citizenship = South Africa, Country of Origin = South Africa
6. Set Client Classification = Development, Marital Status = Single
7. Searched for address "Marshalltown Johannesburg" → selected "Marshalltown, Johannesburg, South Africa" from Google Places
8. Province and Region auto-populated from Google Places
9. Saved

### Assertions
- [x] Client ID Number = 7708206169188
- [x] Name = Ian Houvet
- [x] Residential Address = Marshalltown, Johannesburg, South Africa
- [x] Province = Gauteng
- [x] Region = Central Region

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Opportunity detail](screenshots/e2e-personal-loan-application-ci-23260437980/tc03-opportunity-detail.png) | Opportunity detail page |
| ![Address search](screenshots/e2e-personal-loan-application-ci-23260437980/tc03-address-search.png) | Address search input |
| ![Address suggestions](screenshots/e2e-personal-loan-application-ci-23260437980/tc03-address-suggestions.png) | Google Places suggestions |
| ![Client info filled](screenshots/e2e-personal-loan-application-ci-23260437980/tc03-client-info-filled.png) | Client info form filled |
| ![Client info saved](screenshots/e2e-personal-loan-application-ci-23260437980/tc03-client-info-saved.png) | Client info saved |

### Input vs Output
| Field | Input | Output |
|-------|-------|--------|
| Client ID | 7708206169188 | 7708206169188 |
| Title | Mr | Mr |
| First Name | Ian | Ian |
| Surname | Houvet | Houvet |
| Email | promise.raganya@boxfusion.io | promise.raganya@boxfusion.io |
| Mobile | 0712345678 | 0712345678 |
| Address | Marshalltown Johannesburg (search) | Marshalltown, Johannesburg, South Africa |
| Province | (auto) | Gauteng |
| Region | (auto) | Central Region |
| Classification | Development | Development |
| Marital Status | Single | Single |

### UX Observation
> **UX-01:** After saving Client Info, Province and Region display as "unknown" in the read-only view, but correctly show "Gauteng" and "Central Region" when the form is reopened in edit mode. This is a rendering issue in the read-only view — the data is saved correctly. Recommend investigating the read-only display component for these fields.

---

## TC-04: Fill Loan Info

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-details?id=46a5e90f-9f11-4af5-a2d0-959c14e2eeef

### Steps Followed
1. Clicked Edit → Loan Info tab
2. Selected Product: "R MT Loans CB&T" via ellipsis picker (double-click to select)
3. Filled Business Summary: "Farming operations in Gauteng region"
4. Set Requested Amount: 500000
5. Set Existing Relationship with Bank: None
6. Set Sources Of Income: Farming income
7. Added Loan Purpose row: Purpose = "Purchase Of Livestock", Amount = 500000
8. Saved

### Assertions
- [x] Product = R MT Loans (CB&T)
- [x] Requested Amount = 500000
- [x] Loan Purpose row: Purchase Of Livestock — 500000
- [x] Data saved successfully

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Loan info filled](screenshots/e2e-personal-loan-application-ci-23260437980/tc04-loan-info-filled.png) | Loan info form filled |
| ![Loan info saved](screenshots/e2e-personal-loan-application-ci-23260437980/tc04-loan-info-saved.png) | Loan info saved |

### Input vs Output
| Field | Input | Output |
|-------|-------|--------|
| Product | R MT Loans CB&T | R MT Loans |
| Business Summary | Farming operations in Gauteng region | Farming operations in Gauteng region |
| Requested Amount | 500000 | 500000 |
| Existing Relationship | None | None |
| Sources of Income | Farming income | Farming income |
| Loan Purpose | Purchase Of Livestock | Purchase Of Livestock |
| Loan Purpose Amount | 500000 | 500000 |

---

## TC-05a: Negative — Initiate with Requested Amount = 0

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-details?id=46a5e90f-9f11-4af5-a2d0-959c14e2eeef

### Steps Followed
1. Edited Requested Amount to 0 and saved
2. Clicked "Initiate Loan Application"
3. Observed error toast

### Assertions
- [x] Error: "Cannot initiate workflow: requested amount must be greater than zero."
- [x] Status remains "Draft"

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Amount zero error](screenshots/e2e-personal-loan-application-ci-23260437980/tc05a-amount-zero-error.png) | Error: amount must be > 0 |

---

## TC-05b: Negative — Initiate without Product

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-details?id=46a5e90f-9f11-4af5-a2d0-959c14e2eeef

### Steps Followed
1. Restored Amount = 500000, removed R MT Loans product, saved
2. Clicked "Initiate Loan Application"
3. Observed error toast

### Assertions
- [x] Error: "Cannot initiate workflow: at least one product is required."
- [x] Status remains "Draft"

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![No product error](screenshots/e2e-personal-loan-application-ci-23260437980/tc05b-no-product-error.png) | Error: at least one product required |

---

## TC-05: Initiate Loan Application (Happy Path)

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-details?id=46a5e90f-9f11-4af5-a2d0-959c14e2eeef

### Steps Followed
1. Restored Product = R MT Loans CB&T, confirmed Amount = 500000, saved
2. Clicked "Initiate Loan Application"
3. Verified success toast and status change

### Assertions
- [x] Toast: "Loan Application submitted successfully"
- [x] Status changed to "Verification In Progress"
- [x] Workflow item appeared in Inbox (LA2026/0943)

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Loan initiated](screenshots/e2e-personal-loan-application-ci-23260437980/tc05-loan-initiated.png) | Status: Verification In Progress |

### Input vs Output
| Field | Before | After |
|-------|--------|-------|
| Status | Draft | Verification In Progress |
| Workflow | — | LA2026/0943 in Inbox |

---

## TC-06: Review and Finalise Verification Outcomes

**URL:** https://landbankcrm-adminportal-qa.shesha.app/shesha/workflow-action?id=17496341-a44e-4344-b6ee-cf270cc72bf9&todoid=cd8dcbd4-b879-4a37-bf67-c045e8a93208

### Steps Followed
1. Navigated to Inbox
2. Located LA2026/0943 — "Confirm verification outcomes" (received 18/03/2026 20:38)
3. Clicked search icon to open workflow action page
4. Clicked "Awaiting Review" button for Ian Houvet (Main Applicant)
5. Reviewed **Overview** tab: ID Status = Completed, Photo Verification = Awaiting Review, KYC Status = Completed, Compliance = Completed
6. Reviewed **ID Verification** tab: Status = Completed, Date = 18/03/2026, Name Match = Passed, ID Match = Passed, Death Check = Passed, Outcome = Passed
7. Reviewed **KYC Verification** tab: Status = Completed, First Name Match = Passed, Outcome = Passed
8. Closed the verification dialog
9. Clicked "Finalise Verification Outcomes"
10. Workflow advanced to "Complete Onboarding Checklist"

### Assertions
- [x] Workflow item found in Inbox for LA2026/0943
- [x] "Awaiting Review" button clicked and dialog opened
- [x] All 3 tabs reviewed (Overview, ID Verification, KYC Verification)
- [x] ID Verification: Outcome = Passed
- [x] KYC Verification: Outcome = Passed
- [x] Finalise succeeded — workflow advanced to next step

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Inbox](screenshots/e2e-personal-loan-application-ci-23260437980/tc06-inbox.png) | Inbox with LA2026/0943 |
| ![Verify action page](screenshots/e2e-personal-loan-application-ci-23260437980/tc06-verify-action-page.png) | Verification action page |
| ![Overview tab](screenshots/e2e-personal-loan-application-ci-23260437980/tc06-verify-overview-tab.png) | Overview: statuses |
| ![ID Verification tab](screenshots/e2e-personal-loan-application-ci-23260437980/tc06-verify-id-tab.png) | ID Verification: Completed, face photo |
| ![KYC Verification tab](screenshots/e2e-personal-loan-application-ci-23260437980/tc06-verify-kyc-tab.png) | KYC Verification: Completed |
| ![Onboarding start](screenshots/e2e-personal-loan-application-ci-23260437980/tc06-finalised-tc07-start.png) | After finalise — onboarding checklist opened |

### Verification Summary
| Check | Result |
|-------|--------|
| ID Status | Completed |
| Photo Verification Status | Awaiting Review |
| KYC Status | Completed |
| Compliance Verification | Completed |
| ID Match | Passed |
| Name Match | Passed |
| Death Check | Passed |
| ID Verification Outcome | Passed |
| KYC First Name Match | Passed |
| KYC Outcome | Passed |

### UX Observation
> **UX-02:** Photo Verification Status shows "Awaiting Review" on the Overview tab while ID and KYC are both "Completed". This may indicate photo verification requires manual review. No blocker for workflow progression.

---

## TC-07: Fill and Submit Onboarding Checklist

**URL:** https://landbankcrm-adminportal-qa.shesha.app/shesha/workflow-action?id=17496341-a44e-4344-b6ee-cf270cc72bf9&todoid=60c37cde-656c-48ea-b40a-1036a8109199

### Steps Followed
1. Arrived on "Complete Onboarding Checklist" page (auto-navigated after TC-06 finalise)
2. Set Years of Farming Experience = "4 to 6 Years"
3. Checked: Does this operation require Water Use Rights? = Yes
4. Checked conditional: Support with applying for water rights required? = Yes
5. Checked: Business Plan Development Support required? = Yes
6. Checked: Is there access to working Equipment and Mechanization? = Yes
7. Checked: Does the client have a Valid Tax Clearance certificate? = Yes
8. Checked: Does the client have access to established markets? = Yes
9. Checked: Formal Financial Records or Statements maintained? = Yes
10. Checked: Does the client have an actively engaged Mentor? = Yes
11. Checked: Is the client Compliant with all applicable Labor Laws? = Yes
12. Clicked Submit
13. Verified "Checklist saved successfully." toast
14. Verified workflow status = Completed
15. Verified opportunity status = Complete

### Assertions
- [x] Years of Farming Experience = 4 to 6 Years
- [x] All checkboxes checked (including conditional water rights support)
- [x] Submit succeeded: "Checklist saved successfully."
- [x] Workflow LA2026/0943 → Status: Completed (visible in My Items)
- [x] Opportunity AutoCI23260437980 Houvet → Status: Complete

### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Checklist filled](screenshots/e2e-personal-loan-application-ci-23260437980/tc07-checklist-filled.png) | All checkboxes checked, form filled |
| ![Workflow completed](screenshots/e2e-personal-loan-application-ci-23260437980/tc07-workflow-completed.png) | My Items: LA2026/0943 = Completed |
| ![Opportunity complete](screenshots/e2e-personal-loan-application-ci-23260437980/tc07-opportunity-complete.png) | Opportunity status: Complete |

### Input vs Output
| Field | Input | Output |
|-------|-------|--------|
| Years of Farming Experience | 4 to 6 Years | 4 to 6 Years |
| Water Use Rights | Yes | Yes |
| Water Rights Support | Yes | Yes |
| Business Plan Support | Yes | Yes |
| Equipment & Mechanization | Yes | Yes |
| Tax Clearance | Yes | Yes |
| Established Markets | Yes | Yes |
| Financial Records | Yes | Yes |
| Mentor Engaged | Yes | Yes |
| Labour Law Compliance | Yes | Yes |
| Workflow Status | In Progress | **Completed** |
| Opportunity Status | Verification In Progress | **Complete** |

---

## UX Observations Summary

| ID | Severity | Description | Steps to Reproduce |
|----|----------|-------------|--------------------|
| UX-01 | Low | Province/Region display as "unknown" in read-only view after saving Client Info, but data is correct in edit mode. Affects visual verification. | TC-03: Save Client Info → view read-only page |
| UX-02 | Info | Photo Verification Status shows "Awaiting Review" while ID and KYC show "Completed". May require manual photo review step. | TC-06: Open Awaiting Review dialog → Overview tab |

---

## Recommendations

1. **Fix read-only rendering for Province/Region** (UX-01): The fields render as "unknown" after save. Likely a display binding issue in the read-only component — does not affect data integrity but confuses reviewers.
2. **Clarify Photo Verification status** (UX-02): Document whether "Awaiting Review" for Photo Verification is expected behaviour or requires a separate manual action.
3. **No test plan updates needed**: All UI elements matched the test plan steps. No discrepancies between plan and actual UI.

---

## RESULT: PASS

All 9 test cases (TC-01 through TC-07 including TC-05a and TC-05b negatives) passed. The full E2E personal loan application workflow completed successfully: Lead → Pre-Screening → Opportunity Setup → Initiate Loan → Verify → Onboarding → **Complete**.
