# E2E Personal Loan Application — Test Report (Run 3)

**Date:** 2026-03-18
**Test Plan:** test-plans/e2e-personal-loan-application.md
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
| Duration      | ~15m        |

---

## Test Data

| Item | Value |
|------|-------|
| Unique Lead Name | Ian15224 |
| Lead ID | a6016598-c006-4065-9e6e-79979ee22b37 |
| Lead Ref | LD-2026-000723 |
| Opportunity ID | f9925f7f-9f3e-45c1-aa50-e8781772160e |
| Account ID | 05775045-6274-47a1-b853-d1d40dc5f779 |
| Workflow Ref | LA2026/0926 |
| Client ID Number | 7708206169188 |
| Email | promise.raganya@boxfusion.io |

---

## TC-01: Create Individual Lead

### Steps Followed
1. Logged in as admin / ****
2. Navigated to Leads table via sidebar — confirmed 758 items
3. Clicked "New Lead" — dialog opened
4. Filled all fields: Title=Mr, First Name=Ian15224, Last Name=Houvet, Mobile=0712345678, Email=promise.raganya@boxfusion.io, Client Type=Individual (Individual), Province=Gauteng, Preferred Communication=Email, Lead Channel=Employee Referral
5. Clicked OK
6. Confirmed lead at top of table, count now 759, Status: New

### Input vs Output

| Field | Submitted | Returned (on table) | Match |
|-------|-----------|---------------------|-------|
| First Name | Ian15224 | Ian15224 | YES |
| Last Name | Houvet | Houvet | YES |
| Client Type | Individual (Individual) | Individual (Individual) | YES |
| Province | Gauteng | Gauteng | YES |
| Lead Channel | Employee Referral | Employee Referral | YES |
| Lead Status | (auto) | New | YES |
| Item count | 758 before | 759 after | YES |

**Result: PASS**

---

## TC-02: Pre-Screening — All Criteria Pass

### Steps Followed
1. Clicked search icon on Ian15224 row — confirmed header "Houvet, Ian15224", Status: New
2. Clicked "Initiate Pre-Screening" — dialog opened with 7 questions
3. Answered all 7 questions (Q1-3,6-7=Yes, Q4-5=No)
4. Ticked confirmation checkbox — Submit enabled
5. Clicked Submit
6. Confirmed "Pre-assessment passed!" and "Opportunity created!"

### Input vs Output

| Item | Expected | Returned | Match |
|------|----------|----------|-------|
| Pre-assessment | Passed | "Pre-assessment passed!" | YES |
| Opportunity | Created | "Opportunity created!" | YES |
| Lead status | Converted | Converted | YES |
| Assessment | Passed | Passed | YES |
| Converted To Opportunity | Link present | "Ian15224 Houvet" link | YES |
| Converted To Account | Link present | "Ian15224 Houvet" link | YES |

**Result: PASS**

---

## TC-03: Edit Client Info — All Fields Except Marital Regime

### Steps Followed
1. Clicked "Converted To Opportunity" link — navigated to opportunity page
2. Confirmed: "Ian15224 Houvet", Draft, Personal, Opportunity Owner empty
3. Clicked "Edit" — edit mode active
4. Set Opportunity Owner → Fatima Abrahams
5. Cleared Client Name, typed "Ian"
6. Entered Client ID Number: 7708206169188
7. Set Country Of Residence → South Africa
8. Set Citizenship → South Africa
9. Set Country Of Origin → South Africa
10. Set Client Classification → Development
11. Set Residential Address → "100 Main Street, Main Street, Marshalltown, Johannesburg, South Africa" (via Google Places)
12. Set Provincial Office → Provincial Office
13. Set Marital Status → Single
14. Left Marital Regime empty (intentional)
15. Clicked Save — "Data saved successfully!"

### Input vs Output

| Field | Submitted | Returned (after save) | Match |
|-------|-----------|----------------------|-------|
| Opportunity Owner | Fatima Abrahams | Fatima Abrahams | YES |
| Client ID Number | 7708206169188 | 7708206169188 | YES |
| Client Name | Ian | Ian | YES |
| Client Surname | Houvet | Houvet | YES |
| Country Of Residence | South Africa | South Africa | YES |
| Citizenship | South Africa | South Africa | YES |
| Country Of Origin | South Africa | South Africa | YES |
| Client Classification | Development | Development | YES |
| Residential Address | 100 Main Street, Johannesburg | 100 Main Street, Main Street, Marshalltown, Johannesburg, South Africa | YES |
| Province | Gauteng | Gauteng | YES |
| Region | Central Region | Central Region | YES |
| Provincial Office | Provincial Office | Provincial Office | YES |
| Marital Status | Single | Single | YES |
| Marital Regime | (empty) | (empty) | YES |

**Result: PASS**

---

## TC-04: Fill Loan Info — Product, Amount, Purpose

### Steps Followed
1. Clicked Edit → Loan Info tab
2. Clicked ellipsis on Products → entity picker with 17 products
3. Double-clicked "R MT Loans CB&T" → badge appeared
4. Filled Business Summary: "Farming operations in Gauteng region"
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
| Business Summary | Farming operations in Gauteng region | Saved | YES |
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

## TC-06: Confirm Verification Outcomes

### Steps Followed
1. Logged out as admin, logged in as fatima.abrahams@landbank.co.za
2. Navigated to Inbox via sidebar — 233 items
3. First row: LA2026/0926, "Confirm verification outcomes", In Progress
4. Clicked search icon — workflow page loaded
5. Verified Client Info read-only (all correct)
6. Verified Individual Verifications: Ian Houvet, TBD, "Awaiting Review" button
7. **Clicked "Awaiting Review"** — dialog opened
8. **Overview tab:** ID Status=Completed, Photo=Awaiting Review, KYC=Completed, Compliance=Completed
9. **ID Verification tab:** Submitted=Ian Houvet/7708206169188, Returned=IAN HOUVET/7708206169188/20/08/1977/Male, Name Match=Passed, ID Match=Passed, Death Check=Passed, Outcome=Passed
10. **KYC Verification tab:** Submitted=7708206169188, Returned=IAN/7708206169188/34 VINCENT AVE/BOXFUSION, First Name Match=Passed, Outcome=Passed
11. **Closed dialog**
12. Clicked "Finalise Verification Outcomes"
13. Redirected to "Complete Onboarding Checklist: In Progress"

### Input vs Output

| Item | Expected | Returned | Match |
|------|----------|----------|-------|
| Inbox row | LA2026/xxxx, Confirm verification outcomes | LA2026/0926 | YES |
| Awaiting Review button | Opens dialog | Dialog opened with 3 tabs | YES |
| Overview — ID Status | Completed | Completed | YES |
| Overview — Photo | Awaiting Review | Awaiting Review | YES |
| Overview — KYC | Completed | Completed | YES |
| Overview — Compliance | Completed | Completed | YES |
| ID Verification — Outcome | Passed | Passed | YES |
| KYC Verification — Outcome | Passed | Passed | YES |
| After Finalise | Onboarding Checklist | "Complete Onboarding Checklist: In Progress" | YES |

**Result: PASS**

---

## TC-07: Complete Onboarding Checklist

### Steps Followed
1. Confirmed "Complete Onboarding Checklist: In Progress", LA2026/0926
2. Selected Years Of Farming Experience: "4 to 6 Years"
3. Checked all 9 checkboxes (including conditional Water Use Rights support)
4. Verified 0 unchecked remaining
5. Clicked Submit — "Checklist saved successfully."
6. Workflow completed: "loan-application-workflow: Completed"
7. "Requested action is not available"

### Input vs Output

| Field | Submitted | Returned | Match |
|-------|-----------|----------|-------|
| Years Of Farming Experience | 4 to 6 Years | Selected | YES |
| All 9 checkboxes | Checked | Checked (0 unchecked) | YES |
| Submit | Clicked | "Checklist saved successfully." | YES |
| Workflow status | Completed | "loan-application-workflow: Completed" | YES |
| Post-completion | No more actions | "Requested action is not available" | YES |

**Result: PASS**

---

## TC-08: Verify Opportunity Status is Complete

### Steps Followed
1. Navigated to Opportunities table via sidebar
2. First row: Ian15224 Houvet, Complete, Fatima Abrahams, Personal, Gauteng

### Input vs Output

| Field | Expected | Displayed | Match |
|-------|----------|-----------|-------|
| Application Status | Complete | Complete | YES |
| Account | Ian15224 Houvet | Ian15224 Houvet | YES |
| Application Type | Personal | Personal | YES |
| Opportunity Owner | Fatima Abrahams | Fatima Abrahams | YES |
| Province | Gauteng | Gauteng | YES |
| From Lead | LD-2026-000723 | LD-2026-000723 | YES |

**Result: PASS**

---

## Issues Found

| # | TC | Severity | Description |
|---|-----|----------|-------------|
| 1 | All | Low | **Console errors persist** — `executeScriptSync error TypeError: Cannot read properties` throughout all steps. Does not block functionality. |
| 2 | TC-06 | Info | **Photo Verification "Awaiting Review"** — while ID and KYC show "Completed". Workflow allows finalisation regardless. |

---

## Run Comparison

| Item | Run 1 (2026-03-17) | Run 2 (2026-03-18) | Run 3 (2026-03-18) |
|------|--------------------|--------------------|---------------------|
| Lead Name | Ian53362 | Ian79374 | Ian15224 |
| Workflow Ref | LA2026/0894 | LA2026/0924 | LA2026/0926 |
| TC-06 Review | SKIPPED | COMPLETED | COMPLETED |
| Result | 7P / 1PF | 8P / 0F | **8P / 0F** |

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
