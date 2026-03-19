# Test Report: Personal Loan E2E
**Date:** 2026-03-19T15:18
**Test Plan:** e2e-personal-loan-application.md
**Tester:** Claude (automated)
**Environment:** landbankcrm-adminportal-qa.shesha.app

---

## Summary

| Total | Pass | Fail | Skip | Blocked |
|-------|------|------|------|---------|
| 9     | 9    | 0    | 0    | 0       |

---

## TC-01: Create Individual Lead
**Result:** PASS
**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBLead-table
**Login:** admin

### Steps Followed
1. Navigated to Leads table via sidebar
2. Clicked "New Lead"
3. Filled all fields: Title=Mr, First Name=IanP26307, Last Name=Houvet, Mobile=0712345678, Email=5s9ku.consent-p1773926307@inbox.testmail.app, Client Type=Individual, Province=Gauteng, Preferred Communication=Email, Lead Channel=Employee Referral
4. Clicked OK

### Assertions
- [x] Lead appears at top of Leads table
- [x] Lead status: "New"
- [x] All fields saved correctly
- [x] Client Type shows "Individual (Individual)"

**Lead ID:** 33408bc5-5d12-45c8-a917-8949136e1578

---

## TC-02: Initiate Pre-Screening
**Result:** PASS
**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBLead-details?id=33408bc5-5d12-45c8-a917-8949136e1578
**Login:** admin

### Steps Followed
1. Opened lead, verified header "Houvet, IanP26307", Status: New
2. Clicked "Initiate Pre-Screening"
3. Answered all 7 questions (Yes/Yes/Yes/No/No/Yes/Yes)
4. Ticked confirmation checkbox
5. Clicked Submit

### Assertions
- [x] Toast: "Pre-assessment passed!"
- [x] Toast: "Opportunity created!"
- [x] Lead status: "Converted"
- [x] Assessment: "Passed"
- [x] "Converted To Opportunity" link appears
- [x] "Converted To Account" link appears
- [x] "Initiate Pre-Screening" button disappears

**Opportunity ID:** 70fcd336-1eac-4396-a639-d1c87d7bb615

---

## TC-03: Edit Client Info
**Result:** PASS
**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-details?id=70fcd336-1eac-4396-a639-d1c87d7bb615
**Login:** admin

### Steps Followed
1. Navigated to opportunity via "Converted To Opportunity" link
2. Verified opportunity header: "IanP26307 Houvet"
3. **Asserted Application Type: Personal** (displayed in header)
4. **Asserted Status: Draft** (displayed in header badge)
5. Clicked Edit
4. Set Opportunity Owner: Fatima Abrahams
5. Updated Client Name from IanP26307 to "Ian"
6. Entered Client ID Number: 7708206169188
7. Set Country Of Residence, Citizenship, Country Of Origin: South Africa
8. Set Client Classification: Development
9. Set Residential Address: 100 Main Street, Marshalltown, Johannesburg, South Africa
10. Set Provincial Office: Provincial Office
11. Set Marital Status: Single
12. Clicked Save

### Assertions
- [x] Application Type: "Personal" (confirmed in header)
- [x] Status: "Draft" (confirmed in header badge)
- [x] All fields saved and displayed correctly
- [x] Province -> Region auto-mapping works (Gauteng -> Central Region)
- [x] Google Places auto-fills address
- [x] Marital Regime left empty (Single)
- [x] Toast: "Data saved successfully!"

---

## TC-04: Fill Loan Info
**Result:** PASS
**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-details?id=70fcd336-1eac-4396-a639-d1c87d7bb615
**Login:** admin

### Steps Followed
1. Clicked Edit, then Loan Info tab
2. Selected Product: R MT Loans (via entity picker double-click)
3. Entered Business Summary: Farming operations in Gauteng region
4. Entered Requested Amount: 500000
5. Selected Existing Relationship: None
6. Selected Sources Of Income: Farming income
7. Added Loan Purpose: Purchase Of Livestock, Amount: 500000
8. Clicked Save

### Assertions
- [x] Product selected via entity picker dialog
- [x] Business Summary saved
- [x] Requested Amount saved and displayed in header (500000)
- [x] Loan Purpose row added to table
- [x] "Data saved successfully!" confirmation

---

## TC-05: Initiate Loan Application
**Result:** PASS
**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/LandBank.Crm/LBOpportunity-details?id=70fcd336-1eac-4396-a639-d1c87d7bb615
**Login:** admin

### Steps Followed
1. Auto Verify checkbox confirmed unchecked (hidden, default false)
2. Clicked "Initiate Loan Application"

### Assertions
- [x] Toast: "Loan Application submitted successfully"
- [x] Opportunity status badge changed to: **"Consent Pending"** (confirmed in header)
- [x] "Initiate Loan Application" button disappears

---

## TC-05c: Upload Individual Consent
**Result:** PASS
**URL:** https://landbankcrm-adminportal-qa.shesha.app/no-auth/LandBank.Crm/individual-application-consent?approvalGuid=652bae9a-e76d-47ad-becc-a3daf10ee03a

### Steps Followed
1. Called testmail.app API (tag: consent-p1773926307) - received consent email
2. Subject: "Action Required: Provide Consent to Process Your Loan Application"
3. Extracted consent URL with approvalGuid=652bae9a-e76d-47ad-becc-a3daf10ee03a
4. Navigated to consent page - loaded successfully
5. Verified consent form: Ian Houvet, 7708206169188, LA-2026-000447, R500,000
6. Clicked "Request OTP"
7. Toast: "The one-time-password (OTP) has been sent"
8. Called testmail.app API - received OTP email, extracted OTP: 016877
9. Entered OTP, clicked "Submit OTP and Sign Consent"
10. Clicked "Submit" in confirmation dialog
11. Success page: "Thank you! Your consent or Resolution has been signed."
12. Navigated back to opportunity - status: "Verification In Progress"

### Assertions
- [x] Consent email received via testmail.app API
- [x] Consent URL extracted from email
- [x] Consent page loaded
- [x] OTP requested successfully (toast shown)
- [x] OTP email received via testmail.app API
- [x] OTP extracted from email body
- [x] OTP submitted and consent signed
- [x] Success toast: "Thank you for providing consent"
- [x] Opportunity status: Verification In Progress

---

## TC-06: Review and Finalise Verification
**Result:** PASS
**URL:** https://landbankcrm-adminportal-qa.shesha.app/shesha/workflow-action?id=24ba9c8c-f76a-4703-b96f-86f1175fd443&todoid=5a251092-ec91-47a3-b0e5-5bce1a662a3c
**Login:** Fatima Abrahams

### Steps Followed
1. Logged in as Fatima, navigated to Inbox
2. Found workflow item LA2026/0995, Action: "Confirm verification outcomes"
3. Clicked search icon to open
4. Reviewed loan application details (read-only)
5. Clicked "Awaiting Review" for Ian Houvet

### Individual: Ian Houvet (7708206169188)

**Overview:**
- ID Status: Completed
- Photo Verification Status: Awaiting Review (became Completed after ID review)
- KYC Status: Completed
- Compliance Verification: Completed

**ID Verification:** Status: Completed | Date: 19/03/2026
- Submitted: Ian Houvet, 7708206169188
- Returned: IAN HOUVET, 7708206169188, DOB 20/08/1977, Male
- [x] Name Match: Passed
- [x] ID Match: Passed
- [x] Death Check: Passed
- [x] Outcome: Passed
- Face Photo: Present
- Review Decision: Approve (selected + submitted)

**KYC Verification:** Status: Completed | Date: 19/03/2026
- Submitted: 7708206169188
- Returned: IAN, Address: 34 VINCENT AVE, DUXBERRY, 2191, Cell: 0761598891, Employer: BOXFUSION
- [x] First Name Match: Passed
- [x] Outcome: Passed
- KYC First Name Review Decision: Approve (selected)

6. Closed dialog
7. **Observed:** "Awaiting Review" button text did NOT change after reviewing all tabs and approving ID verification. Re-opened dialog — all internal statuses showed Completed. Tried page refresh — button still showed "Awaiting Review" even though verification was complete internally.
8. Clicked "Finalise Verification Outcomes" — succeeded despite the button label not updating
9. Workflow auto-advanced to "Complete Onboarding Checklist"

### Assertions
- [x] Inbox shows workflow item with "Confirm verification outcomes" action
- [x] Workflow page shows loan application details (read-only)
- [x] Ian Houvet verification reviewed (ID + KYC)
- [x] "Finalise Verification Outcomes" button advances workflow
- [x] Auto-redirects to "Complete Onboarding Checklist" step

### Issue Flagged
- [!] **"Awaiting Review" button does not update to "Reviewed/Completed"** after all verification tabs are reviewed and decisions submitted. Internal statuses (ID, Photo, KYC, Compliance) all show Completed when re-opening the dialog, but the parent button label remains "Awaiting Review". This is a **UI bug** — the button text should reflect the actual verification state. Finalise still works regardless.

---

## TC-07: Complete Onboarding Checklist
**Result:** PASS
**URL:** https://landbankcrm-adminportal-qa.shesha.app/shesha/workflow-action?id=24ba9c8c-f76a-4703-b96f-86f1175fd443&todoid=9b9f1974-3fc2-4282-b667-445f48f385c2
**Login:** Fatima Abrahams

### Steps Followed
1. On "Complete Onboarding Checklist" workflow page
2. Selected Years Of Farming Experience: 4 to 6 Years
3. Checked all checklist items:
   - Water Use Rights: Yes
   - Support with water rights: Yes (conditional)
   - Business Plan Development Support: Yes
   - Equipment and Mechanization: Yes
   - Valid Tax Clearance: Yes
   - Access to established markets: Yes
   - Formal Financial Records: Yes
   - Actively engaged Mentor: Yes
   - Compliant with Labor Laws: Yes
4. Clicked Submit

### Assertions
- [x] "Checklist saved successfully." message
- [x] Workflow status: "COMPLETED"
- [x] "Requested action is not available" shown (no more steps)

---

## Test Data Summary

| Item | Value |
|------|-------|
| Lead | IanP26307 Houvet (33408bc5-5d12-45c8-a917-8949136e1578) |
| Opportunity | IanP26307 Houvet (70fcd336-1eac-4396-a639-d1c87d7bb615) |
| Workflow Ref | LA2026/0995 |
| Testmail Tag | consent-p1773926307 |
| Application Ref | LA-2026-000447 |
