# E2E Entity (Close Corporation) Loan Application — Test Report (Run 1)

**Date:** 2026-03-18
**Test Plan:** test-plans/e2e-entity-loan-application.md
**Tester:** Claude (AI-driven, manual browser execution via MCP Playwright tools)
**Accounts:** admin (Phase 1–3), fatima.abrahams@landbank.co.za (Phase 4–8)
**Environment:** QA — landbankcrm-adminportal-qa.shesha.app

---

## Run Summary

| Field          | Value       |
|---------------|-------------|
| Date          | 2026-03-18  |
| Total cases   | 8           |
| Passed        | 8           |
| Failed        | 0           |
| Skipped       | 0           |
| Duration      | ~20m        |

---

## Test Data

| Item | Value |
|------|-------|
| Unique Lead Name | Entity76374 |
| Lead ID | 5b7040cf-9d81-41f2-8c57-da7f58d50ce7 |
| Lead Ref | LD-2026-000730 |
| Opportunity ID | 426146be-755f-48c7-8fdb-64c2beab46ed |
| Account ID | 1ce57116-cd06-4ba4-8718-ac2c21b95107 |
| Workflow Ref | LA2026/0938 |
| Entity Name | Boxfusion Entity76374 |
| Company Reg | 2012/225386/07 |
| Email | promise.raganya@boxfusion.io |

---

## TC-01: Create Close Corporation (Entity) Lead

### Steps Followed
1. Logged in as admin / ****
2. Navigated to Leads table via sidebar — confirmed 765 items
3. Clicked "New Lead" — dialog opened
4. Filled all fields: Title=Mr, First Name=Entity76374, Last Name=Houvet, Mobile=0712345678, Email=promise.raganya@boxfusion.io, Client Type=Close Corporation (Entity), Entity Name=Boxfusion Entity76374, Province=Gauteng, Preferred Communication=Email, Lead Channel=Employee Referral
5. Clicked OK
6. Confirmed lead at top of table, count now 766, Status: New

### Input vs Output

| Field | Submitted | Returned (on table) | Match |
|-------|-----------|---------------------|-------|
| First Name | Entity76374 | Entity76374 | YES |
| Last Name | Houvet | Houvet | YES |
| Client Type | Close Corporation (Entity) | Close Corporation (Entity) | YES |
| Entity Name | Boxfusion Entity76374 | Boxfusion Entity76374 | YES |
| Province | Gauteng | Gauteng | YES |
| Lead Channel | Employee Referral | Employee Referral | YES |
| Lead Status | (auto) | New | YES |
| Item count | 765 before | 766 after | YES |

**Result: PASS**

---

## TC-02: Pre-Screening — All Criteria Pass

### Steps Followed
1. Opened lead — confirmed header "Houvet, Entity76374", Status: New, Close Corporation (Entity)
2. Clicked "Initiate Pre-Screening" — dialog opened with 7 questions
3. Answered all 7 questions (Q1-3,6-7=Yes, Q4-5=No)
4. Ticked confirmation checkbox — Submit enabled
5. Clicked Submit
6. Confirmed "Pre-assessment passed!" and "Opportunity created!"
7. Status: Converted, Assessment: Passed
8. Converted To Opportunity and Account links appeared

### Input vs Output

| Item | Expected | Returned | Match |
|------|----------|----------|-------|
| Pre-assessment | Passed | "Pre-assessment passed!" | YES |
| Opportunity | Created | "Opportunity created!" | YES |
| Lead status | Converted | Converted | YES |
| Assessment | Passed | Passed | YES |
| Converted To Opportunity | Link present | Link present | YES |
| Converted To Account | Link present | Link present | YES |

**Result: PASS**

---

## TC-03: Edit Entity Info + Directors + Signatories

### Steps Followed
1. Clicked "Converted To Opportunity" link — navigated to opportunity page
2. Confirmed: "Entity76374 Houvet", Draft, Entity type
3. Clicked "Edit" — edit mode active
4. Set Opportunity Owner → Fatima Abrahams
5. Entered Company Registration Number: 2012/225386/07
6. Set Country Of Residence → South Africa
7. Set Citizenship → South Africa
8. Set Client Classification → Development
9. Set Registered Address → "100 Main Street, Main Street, Marshalltown, Johannesburg, South Africa" (via Google Places)
10. Set Provincial Office → Provincial Office
11. Clicked Save — "Data saved successfully!"
12. Added Director 1: Ian Houvet, 7708206169188, all countries South Africa, Married, Married in Community of Property, Spouse: Chamaine Houvet (7304190225085, chamaine.houvet@boxfusion.io) — "Director added successfully."
13. Added Director 2: Chamaine Houvet, 7304190225085, all countries South Africa, Single — "Director added successfully."
14. Added Director 3: Xolile Ndlangana, 6311115651080, all countries South Africa, Single — "Director added successfully."
15. Added Signatory: Ian Houvet, 7708206169188, promise.raganya@boxfusion.io, 0712345678 — "Signatory added successfully."
16. Confirmed all 3 directors and 1 signatory in tables

### Input vs Output

| Field | Submitted | Returned (after save) | Match |
|-------|-----------|----------------------|-------|
| Opportunity Owner | Fatima Abrahams | Fatima Abrahams | YES |
| Company Registration Number | 2012/225386/07 | 2012/225386/07 | YES |
| Country Of Residence | South Africa | South Africa | YES |
| Citizenship | South Africa | South Africa | YES |
| Client Classification | Development | Development | YES |
| Registered Address | 100 Main Street, Johannesburg | 100 Main Street, Main Street, Marshalltown, Johannesburg, South Africa | YES |
| Provincial Office | Provincial Office | Provincial Office | YES |
| Director 1 | Ian Houvet / 7708206169188 | Row in directors table | YES |
| Director 2 | Chamaine Houvet / 7304190225085 | Row in directors table | YES |
| Director 3 | Xolile Ndlangana / 6311115651080 | Row in directors table | YES |
| Signatory | Ian Houvet / 7708206169188 | Row in signatories table | YES |

**Result: PASS**

---

## TC-04: Fill Loan Info — Product, Amount, Purpose

### Steps Followed
1. Clicked Edit → Loan Info tab
2. Clicked ellipsis on Products → entity picker opened
3. Double-clicked "R MT Loans" → badge appeared
4. Filled Business Summary: "Boxfusion farming operations in Gauteng"
5. Filled Requested Amount: 500000
6. Selected Existing Relationship: None
7. Selected Sources Of Income: Farming income
8. Selected Loan Purpose: Purchase Of Livestock, Amount: 500000
9. Clicked plus-circle → row added
10. Clicked Save — "Data saved successfully!", Amount 500000 in header

### Input vs Output

| Field | Submitted | Returned | Match |
|-------|-----------|----------|-------|
| Products | R MT Loans | R MT Loans badge | YES |
| Business Summary | Boxfusion farming operations in Gauteng | Saved | YES |
| Requested Amount | 500000 | 500000 (header) | YES |
| Existing Relationship | None | None | YES |
| Sources Of Income | Farming income | Farming income | YES |
| Loan Purpose | Purchase Of Livestock / 500000 | Row in table | YES |

**Result: PASS**

---

## TC-05: Initiate Loan Application

### Steps Followed
1. Clicked "Initiate Loan Application"
2. Confirmed success message and status change

### Input vs Output

| Item | Expected | Returned | Match |
|------|----------|----------|-------|
| Success message | "Loan Application submitted successfully" | "Loan Application submitted successfully" | YES |
| Status | Verification In Progress | Verification In Progress | YES |
| Initiate button | Removed | Not visible | YES |

**Result: PASS**

---

## TC-06: Confirm Verification Outcomes (Entity)

### Steps Followed
1. Logged out as admin, logged in as fatima.abrahams@landbank.co.za
2. Navigated to Inbox via sidebar
3. Found row: LA2026/0938, "Confirm verification outcomes", In Progress
4. Clicked search icon — workflow page loaded
5. Verified Entity Verifications section:
   - Entity: Compliance Status: Completed
   - Entity Name: Boxfusion Entity76374, CIPC Status with "Awaiting Review" button
   - Signatories: Ian Houvet (7708206169188)
   - Directors: Chamaine Houvet, Xolile Ndlangana, Ian Houvet (all 3 listed)
6. **Clicked "Awaiting Review"** — CIPC Verification dialog opened
7. **Dialog contents:** Status: Awaiting Review, Date: 18/03/2026
8. **Reason for Failure:** "Company name mismatch: Trade name '', Company name 'BOXFUSION (PTY)LTD'"
9. **Submitted:** Reg 2012/225386/07, Company Name: Boxfusion Entity76374
10. **CIPC Returned:** K2012/225386/07, BOXFUSION (PTY)LTD, In Business, Requires Review, Private Company, VAT 4760252900, Age 13 Years 3 Months, Reg Date 2012-12-19, Physical Address: International Business Gateway, New Road Midridge Park, Midrand, Gauteng, 1684
11. Closed dialog
12. Clicked "Finalise Verification Outcomes"
13. Redirected to "Complete Onboarding Checklist: In Progress"

### Input vs Output

| Item | Expected | Returned | Match |
|------|----------|----------|-------|
| Inbox row | LA2026/xxxx, Confirm verification outcomes | LA2026/0938 | YES |
| Entity Compliance | Completed | Completed | YES |
| CIPC Status | Awaiting Review | Awaiting Review | YES |
| CIPC Dialog | Opens with verification data | Dialog opened with CIPC details | YES |
| Directors listed | 3 directors | Chamaine Houvet, Xolile Ndlangana, Ian Houvet | YES |
| Signatories listed | 1 signatory | Ian Houvet (7708206169188) | YES |
| After Finalise | Onboarding Checklist | "Complete Onboarding Checklist: In Progress" | YES |

**Result: PASS**

---

## TC-07: Complete Onboarding Checklist

### Steps Followed
1. Confirmed "Complete Onboarding Checklist: In Progress", LA2026/0938
2. Selected Years Of Farming Experience: "4 to 6 Years"
3. Checked all checkboxes (9 items + conditional Water Use Rights support = 10 checked)
4. 1 remaining unchecked: disabled "Does the client have a resolution?" from entity info
5. Clicked Submit — "Checklist saved successfully."
6. Workflow completed: "loan-application-workflow: Completed"
7. "Requested action is not available"

### Input vs Output

| Field | Submitted | Returned | Match |
|-------|-----------|----------|-------|
| Years Of Farming Experience | 4 to 6 Years | Selected | YES |
| All checkboxes | 10 checked (1 disabled) | 10 checked, 1 disabled unchecked | YES |
| Submit | Clicked | "Checklist saved successfully." | YES |
| Workflow status | Completed | "loan-application-workflow: Completed" | YES |
| Post-completion | No more actions | "Requested action is not available" | YES |

**Result: PASS**

---

## TC-08: Verify Opportunity Status

### Steps Followed
1. Navigated to Opportunities table via sidebar
2. First row: Entity76374 Houvet, Entity, Complete, Fatima Abrahams, Gauteng, Lead LD-2026-000730

### Input vs Output

| Field | Expected | Displayed | Match |
|-------|----------|-----------|-------|
| Account | Entity76374 Houvet | Entity76374 Houvet | YES |
| Application Type | Entity | Entity | YES |
| Application Status | Complete | Complete | YES |
| Opportunity Owner | Fatima Abrahams | Fatima Abrahams | YES |
| Province | Gauteng | Gauteng | YES |
| From Lead | LD-2026-000730 | LD-2026-000730 | YES |

**Result: PASS**

---

## Issues Found

| # | TC | Severity | Description |
|---|-----|----------|-------------|
| 1 | All | Low | **Console errors persist** — `executeScriptSync error TypeError: Cannot read properties` throughout all steps. Does not block functionality. |
| 2 | TC-06 | Info | **CIPC Verification "Company name mismatch"** — submitted entity name "Boxfusion Entity76374" does not match CIPC returned name "BOXFUSION (PTY)LTD". Workflow allows finalisation regardless. |
| 3 | TC-08 | Info | **Application Status initially appeared blank** — Entity type status took a moment to render on the Opportunities table page. After full page load, status correctly shows "Complete". |
| 4 | TC-03 | Info | **No Country Of Origin field** — Entity form does not include a Country Of Origin field at entity level (only available on individual directors). |

---

## RULES.md Compliance

| Rule | Followed |
|------|----------|
| Read full test plan before browser | YES |
| Check prereqs — login first | YES |
| Navigate and snapshot to confirm | YES |
| Do not guess | YES |
| Snapshot before/after every action | YES |
| For dropdowns: snapshot options then select | YES |
| Never skip assertions | YES |
| Do NOT hardcode credentials | YES |
| Do NOT create records unless required | YES |
| Do NOT skip test cases | YES |
