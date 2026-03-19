# E2E Test Report: Personal Loan Application
**Run ID:** CI-23276371190
**Date:** 2026-03-19
**Time:** 02:22 UTC
**Environment:** QA — https://landbankcrm-adminportal-qa.shesha.app
**Lead Name:** AutoCI23276371190 Houvet
**Loan Ref:** LA2026/0957
**Executed by:** Claude (automated CI)
**Test Plan:** test-plans/e2e-personal-loan-application.md

---

## Summary

| TC | Description | Result |
|----|-------------|--------|
| TC-01 | Create Lead | PASS |
| TC-02 | Pre-Screening | PASS |
| TC-03 | Client Info | PASS |
| TC-04 | Loan Info | PASS |
| TC-05a | Negative: Initiate without amount | PASS |
| TC-05b | Negative: Initiate without product | PASS |
| TC-05 | Initiate Loan Application | PASS |
| TC-06 | Verify & Finalise Verification Outcomes | PASS |
| TC-07 | Complete Onboarding Checklist | PASS |

**Total: 9/9 PASS — 0 FAIL — 0 SKIP**

---

## TC-01: Create Lead

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBLead-table

### Steps Followed
1. Navigated to Leads table (admin session)
2. Clicked "Create New" → Lead creation form opened
3. Filled: First Name=AutoCI23276371190, Last Name=Houvet, ID=7708206169188, Title=Mr, Gender=Male, DOB=1977-08-20, Mobile=0712345678, Email=promise.raganya@boxfusion.io, Preferred Communication=Email, Marital Status=Single
4. Saved — toast "Data saved successfully!" appeared
5. Lead visible in table with status "New"

### Input vs Output
| Field | Input | Displayed |
|-------|-------|-----------|
| First Name | AutoCI23276371190 | AutoCI23276371190 |
| Last Name | Houvet | Houvet |
| ID Number | 7708206169188 | 7708206169188 |
| Status | — | New |

### Assertions
- [x] Lead created with status "New"
- [x] "Data saved successfully!" toast shown
- [x] Lead visible in Leads table

**Result: PASS**

---

## TC-02: Pre-Screening

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBLead-table (Lead detail → Pre-screening tab)

### Steps Followed
1. Opened lead AutoCI23276371190 Houvet from Leads table
2. Navigated to Pre-screening tab
3. Answered: Q1=Yes, Q2=Yes, Q3=Yes, Q4=No, Q5=No, Q6=Yes, Q7=Yes
4. Clicked "Submit Pre-assessment"
5. Toast "Pre-assessment passed!" appeared
6. Toast "Opportunity created!" appeared
7. Lead status changed to "Converted"

### Input vs Output
| Question | Answer | Outcome |
|----------|--------|---------|
| Q1–Q3, Q6, Q7 | Yes | — |
| Q4, Q5 | No | — |
| Overall | — | Pre-assessment passed! |

### Assertions
- [x] "Pre-assessment passed!" message shown
- [x] "Opportunity created!" message shown
- [x] Lead status changed to "Converted"

**Result: PASS**

---

## TC-03: Client Info

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-table (Opportunity → Loan Application → Client Info tab)

### Steps Followed
1. Navigated to Opportunities table
2. Opened opportunity for AutoCI23276371190 Houvet
3. Navigated to Loan Application → Client Info tab
4. Filled all fields: Country=South Africa, Citizenship=South Africa, Country of Origin=South Africa, Client Classification=Development, Residential Address (Google Places)=100 Main Street Marshalltown, Province auto-mapped to Gauteng, Region auto-mapped to Central Region, Provincial Office=Provincial Office
5. Clicked Save — "Data saved successfully!" toast appeared

### Input vs Output
| Field | Input | Displayed |
|-------|-------|-----------|
| Residential Address | 100 Main Street, Marshalltown, Johannesburg, South Africa | Correct |
| Province | (auto) | Gauteng |
| Region | (auto) | Central Region |
| Client Classification | Development | Development |

### Assertions
- [x] "Data saved successfully!" toast shown
- [x] Province auto-mapped to Gauteng
- [x] Region auto-mapped to Central Region

**Result: PASS**

---

## TC-04: Loan Info

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-table (Opportunity → Loan Application → Loan Info tab)

### Steps Followed
1. Navigated to Loan Info tab
2. Selected Product: R MT Loans (CB&T)
3. Entered Requested Amount: 500000
4. Set Existing Relationship with Bank: None
5. Set Sources Of Income: Farming income
6. Added Loan Purpose row: Purpose=Purchase Of Livestock, Amount=500000
7. Entered Business Summary: "Farming operations in Gauteng region"
8. Clicked Save — "Data saved successfully!" toast appeared
9. Confirmed amount "500 000" visible in page header

### Input vs Output
| Field | Input | Displayed |
|-------|-------|-----------|
| Product | R MT Loans (CB&T) | R MT Loans |
| Requested Amount | 500000 | 500 000 (header) |
| Loan Purpose | Purchase Of Livestock | Purchase Of Livestock — 500000 |
| Sources Of Income | Farming income | Farming income |
| Bank Relationship | None | None |

### Assertions
- [x] "Data saved successfully!" toast shown
- [x] Amount 500 000 shown in header
- [x] Loan Purpose row visible in table

**Result: PASS**

---

## TC-05a: Negative — Initiate Without Amount

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-table (Opportunity → Loan Application)

### Steps Followed
1. Temporarily cleared Requested Amount and Loan Purpose amount (set to 0)
2. Clicked "Initiate Loan Application"
3. Error message appeared

### Assertions
- [x] Error: "Cannot initiate workflow: requested amount must be greater than zero."
- [x] Workflow NOT initiated

**Result: PASS**

---

## TC-05b: Negative — Initiate Without Product

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-table (Opportunity → Loan Application)

### Steps Followed
1. Removed product "R MT Loans" from the product selector
2. Clicked "Initiate Loan Application"
3. Error message appeared
4. Restored product (re-selected R MT Loans) and saved before proceeding to TC-05

### Assertions
- [x] Error: "Cannot initiate workflow: at least one product is required."
- [x] Workflow NOT initiated

**Result: PASS**

---

## TC-05: Initiate Loan Application (Happy Path)

**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-table (Opportunity → Loan Application)

### Steps Followed
1. Confirmed Requested Amount=500000, Product=R MT Loans, all fields set
2. Clicked "Initiate Loan Application"
3. Toast "Loan Application submitted successfully" appeared
4. Opportunity status changed to "Verification In Progress"
5. Loan ref assigned: LA2026/0957

### Assertions
- [x] "Loan Application submitted successfully" toast shown
- [x] Status changed to "Verification In Progress"
- [x] Ref No LA2026/0957 assigned

**Result: PASS**

---

## TC-06: Verify & Finalise Verification Outcomes

**URL:** https://landbankcrm-adminportal-qa.shesha.app/shesha/workflow-action?id=698c1e2b-8429-42a9-b51f-ac7a724c7409&todoid=eacce910-f42c-4231-9477-22c190a1ed47

### Steps Followed
1. Logged in as RM (fatima.abrahams@landbank.co.za)
2. Navigated to Inbox → found LA2026/0957, action "Confirm verification outcomes"
3. Clicked search icon to open workflow action page
4. Reviewed read-only loan application details:
   - Client Info: Ian Houvet, 7708206169188, Email=promise.raganya@boxfusion.io, Mobile=0712345678, Province=Gauteng, Region=Central Region
   - Loan Info: R MT Loans, 500000, Purchase Of Livestock, Farming income, None
   - Farms: No data (no farms added)
5. Clicked "Awaiting Review" button for Ian Houvet (Main Applicant)
6. Verification dialog opened — reviewed ALL 3 tabs:
   - **Overview:** ID Status=Completed, Photo Verification=Awaiting Review, KYC Status=Completed, Compliance Verification=Completed
   - **ID Verification:** Ian Houvet, 7708206169188, DOB 20/08/1977, Male — Name Match=Passed, ID Match=Passed, Death Check=Passed, Outcome=Passed
   - **KYC Verification:** ID 7708206169188, First Name IAN, Employer=BOXFUSION — First Name Match=Passed, Outcome=Passed
7. Closed dialog
8. Clicked "Finalise Verification Outcomes"
9. Page navigated to next workflow step: "Complete Onboarding Checklist"

### Assertions
- [x] All 3 verification tabs reviewed (Overview, ID Verification, KYC Verification)
- [x] ID verification: Passed
- [x] KYC verification: Passed
- [x] "Finalise Verification Outcomes" successfully executed
- [x] Workflow advanced to next step

**Result: PASS**

---

## TC-07: Complete Onboarding Checklist

**URL:** https://landbankcrm-adminportal-qa.shesha.app/shesha/workflow-action?id=698c1e2b-8429-42a9-b51f-ac7a724c7409&todoid=f636d077-6094-494c-aefc-f0e8eb3f40d3

### Steps Followed
1. Page loaded automatically after TC-06 finalise — "Complete Onboarding Checklist" workflow step
2. Selected Years Of Farming Experience: **4 to 6 Years**
3. Checked all applicable checkboxes:
   - [x] Does this operation require Water Use Rights? → Yes
   - [x] Support with applying for water rights required? → Yes (conditional, appeared after above)
   - [x] Business Plan Development Support required? → Yes
   - [x] Is there access to working Equipment and Mechanization? → Yes
   - [x] Does the client have a Valid Tax Clearance certificate? → Yes
   - [x] Does the client have access to established markets? → Yes
   - [x] Formal Financial Records or Statements maintained? → Yes
   - [x] Does the client have an actively engaged Mentor? → Yes
   - [x] Is the client Compliant with all applicable Labor Laws? → Yes
4. Clicked Submit
5. Toast "Checklist saved successfully." appeared
6. Redirected to My Items — LA2026/0957 Status = **Completed**

### Assertions
- [x] Years Of Farming Experience = "4 to 6 Years" selected
- [x] All checkboxes checked (including conditional Water Rights support)
- [x] "Checklist saved successfully." toast shown
- [x] LA2026/0957 Status = Completed in My Items

**Result: PASS**

---

## UX Observations

1. **Console errors throughout** — Multiple `executeScriptSync error TypeError: Cannot...` errors appear in the browser console on every page load. These appear to be non-blocking framework-level errors (Shesha internal) but generate significant noise. Not visible to end users but worth investigating.

2. **Photo Verification Status = "Awaiting Review"** — In TC-06, the ID Verification dialog showed Photo Verification as "Awaiting Review" while ID and KYC statuses were Completed. The test plan does not block on this, but the system allowed finalising without a photo review decision. This may be an intentional design (photo is optional) but worth clarifying.

3. **Workflow transition after TC-06** — After clicking "Finalise Verification Outcomes", the API call briefly showed a 500 error in the console (`UserTaskComplete` endpoint), but the workflow still advanced successfully to TC-07. This transient error should be investigated to confirm it is not a reliability risk.

4. **Address autocomplete requires slow typing** — The Google Places API address field does not respond to fast input (paste / fill). Slow character-by-character typing is required to trigger suggestions. This is a UX friction point for users who copy-paste addresses.

---

## Final Results

| Metric | Count |
|--------|-------|
| Total TCs | 9 |
| Passed | 9 |
| Failed | 0 |
| Skipped | 0 |

**RESULT: PASS**
