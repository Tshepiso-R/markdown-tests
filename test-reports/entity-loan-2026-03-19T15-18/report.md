# Test Report: Entity (Close Corporation) Loan E2E
**Date:** 2026-03-19T15:18
**Test Plan:** e2e-entity-loan-application.md
**Tester:** Claude (automated)
**Environment:** landbankcrm-adminportal-qa.shesha.app

---

## Summary

| Total | Pass | Fail | Skip | Blocked |
|-------|------|------|------|---------|
| 10    | 6    | 0    | 0    | 4       |

---

## TC-01: Create Close Corporation (Entity) Lead
**Result:** PASS
**URL:** /dynamic/LandBank.Crm/LBLead-table
**Login:** admin

### Steps Followed
1. Navigated to Leads table via sidebar
2. Clicked "New Lead"
3. Filled fields: Title=Mr, First Name=Entity26307, Last Name=Houvet, Mobile=0712345678, Email=5s9ku.consent-e1773926307@inbox.testmail.app, Client Type=Close Corporation (Entity), Entity Name=Boxfusion, Province=Gauteng, Preferred Communication=Email, Lead Channel=Employee Referral
4. Clicked OK

### Assertions
- [x] Lead appears at top of Leads table
- [x] Lead status: "New"
- [x] Client Type shows "Close Corporation (Entity)"
- [x] All fields saved correctly

**Lead ID:** e1c8773c-a3e5-497a-958f-df670968d97b

---

## TC-02: Initiate Pre-Screening
**Result:** PASS
**Login:** admin

### Steps Followed
1. Opened lead, verified header "Houvet, Entity26307", Status: New
2. Clicked "Initiate Pre-Screening"
3. Answered all 7 questions (Yes/Yes/Yes/No/No/Yes/Yes)
4. Ticked confirmation checkbox, clicked Submit

### Assertions
- [x] Toast: "Pre-assessment passed!"
- [x] Toast: "Opportunity created!"
- [x] Lead status: "Converted", Assessment: "Passed"
- [x] "Converted To Opportunity" and "Converted To Account" links appear

**Opportunity ID:** 038debf5-6b52-460f-be76-3c35bad1c13f

---

## TC-03: Edit Entity Info + TC-04: Fill Loan Info (combined edit session)
**Result:** PASS
**Login:** admin

### Steps Followed
1. Navigated to opportunity via "Converted To Opportunity" link
2. **Asserted Application Type: Entity** (displayed in header)
3. **Asserted Status: Draft** (displayed in header badge)
4. Clicked Edit (single edit session for all fields)
5. Set Opportunity Owner: Fatima Abrahams
6. Filled Entity Info: Entity Name=Boxfusion, Company Registration Number=2012/225386/07, Years In Operation=10
7. Updated Contact Person Name to "Ian"
8. Set Entity Org Type: Closed Corporation (CC), Client Classification: Development, BEEE Level: Level 1
9. Set Country Of Residence + Citizenship: South Africa
10. Set Registered Address: 100 Main Street, Marshalltown, Johannesburg, South Africa
11. Set Provincial Office: Provincial Office
12. Resolution checkbox: initially checked then unchecked (requires document upload — left unchecked)
13. Clicked Save — first attempt failed: "A signed resolution document must be attached when HasResolution is true"
14. Unchecked resolution checkbox, saved successfully

### Assertions
- [x] Application Type: "Entity" (confirmed in header)
- [x] Status: "Draft" (confirmed in header badge)
- [x] All entity fields saved correctly
- [x] Province -> Region auto-mapping works (Gauteng -> Central Region)
- [x] Contact Person fields saved correctly
- [x] Toast: "Data saved successfully!"

**Note:** Resolution checkbox requires uploading a signed document. Left unchecked for this run.

---

## TC-03a: Add Directors
**Result:** PASS
**Login:** admin

### Steps Followed
1. Added Director 1: Ian Houvet (7708206169188), Married in Community of Property, Spouse: Chamaine Houvet (7304190225085)
2. Added Director 2: Chamaine Houvet (7304190225085), Single
3. Added Director 3: Xolile Ndlangana (6311115651080), Single
4. All 3 directors with South Africa for Citizenship/Country Of Residence/Country Of Origin

### Assertions
- [x] Director 1 saved with Married status and spouse details
- [x] Director 2 saved with Single status
- [x] Director 3 saved with Single status
- [x] Marital Regime field only appears when Marital Status = Married
- [x] Spouse fields only appear when Marital Regime = Married in Community of Property
- [x] All 3 directors visible in Directors list

---

## TC-03b: Add Signatories
**Result:** PASS
**Login:** admin

### Steps Followed
1. Clicked "Add Signatory"
2. Filled: Ian Houvet, 7708206169188, testmail email, 0712345678
3. Clicked "Save Signatory"

### Assertions
- [x] Signatory (Ian Houvet) saved with correct details
- [x] Signatory visible in Signatories list

---

## TC-04: Fill Loan Info
**Result:** PASS
**Login:** admin

### Steps Followed
1. Clicked Loan Info tab
2. Selected Product: R MT Loans (via entity picker)
3. Filled Business Summary, Requested Amount: 500000
4. Selected Existing Relationship: None, Sources Of Income: Farming income
5. Added Loan Purpose: Purchase Of Livestock, 500000
6. Clicked Save

### Assertions
- [x] Product selected, Business Summary saved
- [x] Requested Amount: 500000 in header
- [x] Loan Purpose row added
- [x] "Data saved successfully!"

---

## TC-05: Initiate Loan Application
**Result:** PASS (partial — status changed to Resolution Pending)
**Login:** admin

### Steps Followed
1. Auto Verify confirmed unchecked
2. Clicked "Initiate Loan Application"

### Assertions
- [x] Toast: "Loan Application submitted successfully"
- [x] Opportunity status badge changed to: **"Resolution Pending"** (Entity flow requires all directors to sign resolution before consent)
- [x] "Initiate Loan Application" button disappears

**Note:** Entity flow has an additional Resolution step before Consent. Status lifecycle: Draft -> Resolution Pending -> (all directors sign) -> Consent Pending -> (consent signed) -> Verification In Progress. This differs from Personal which goes directly to Consent Pending.

---

## TC-05 (Resolution): Sign Company Resolution
**Result:** PASS (1 of 3 directors signed)

### Steps Followed
1. Retrieved resolution email from testmail (Subject: "Action Required: Company Resolution Needed")
2. Extracted resolution URL (entity-application-resolution-approval?approvalGuid=40cdf5bc...)
3. Navigated to resolution page — verified company details (Boxfusion, 2012/225386/07, LA-2026-000449)
4. Verified 3 directors and 1 signatory listed
5. Clicked "Request OTP", received OTP: 637959
6. Entered OTP, clicked "Submit OTP and Sign Resolution"
7. Confirmed submission
8. Success: "Resolution signed successfully!"

**BLOCKER:** Only Ian's resolution was signed (his email is on testmail). Chamaine (chamaine@boxfusion.io) and Xolile (xolile@boxfusion.io) received resolution emails at non-testmail addresses. ALL directors must sign before the status progresses to Consent Pending.

---

## TC-05c: Upload Entity Consent
**Result:** BLOCKED
**Reason:** Status stuck at "Resolution Pending" — requires ALL 3 directors to sign resolution. Only Ian's signature was completed (testmail). Chamaine and Xolile's emails are at boxfusion.io (not programmatically accessible).

---

## TC-06: Review Entity Verification
**Result:** BLOCKED
**Reason:** Depends on TC-05c (consent flow must complete first)

---

## TC-07: Complete Onboarding Checklist
**Result:** BLOCKED
**Reason:** Depends on TC-06

---

## Test Data Summary

| Item | Value |
|------|-------|
| Lead | Entity26307 Houvet (e1c8773c-a3e5-497a-958f-df670968d97b) |
| Opportunity | Entity26307 Houvet (038debf5-6b52-460f-be76-3c35bad1c13f) |
| Application Ref | LA-2026-000449 |
| Testmail Tag | consent-e1773926307 |
| Directors | Ian Houvet (7708206169188), Chamaine Houvet (7304190225085), Xolile Ndlangana (6311115651080) |
| Signatory | Ian Houvet (7708206169188) |

---

## Recommendations

1. **All director emails should use testmail.app** — Update the test plan to use testmail addresses for ALL directors (not just Ian), so resolution signing can be completed programmatically for all 3.
2. **Update test plan** to document the Resolution step — the entity flow has: Initiate -> Resolution Pending -> (all directors sign) -> Consent Pending -> (consent) -> Verification In Progress. This differs from the personal flow.
3. **Resolution checkbox** requires a document upload — consider testing with the checkbox unchecked (as done here) or providing a test document.
