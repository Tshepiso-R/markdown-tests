# Test Plan: End-to-End Entity (Close Corporation) Loan Application

## Meta
| Field        | Value                                                              |
|-------------|--------------------------------------------------------------------|
| Module      | Full Journey — Lead → Opportunity → Workflow → Complete            |
| URL         | {{BASE_URL}} = landbankcrm-adminportal-qa.shesha.app               |
| Prereqs     | Admin account for lead creation; RM account (Fatima) for workflow   |
| Last tested | 2026-03-18                                                         |
| Status      | Pass                                                               |
| Test Data   | Boxfusion (Entity), Reg: 2012/225386/07, Contact: Ian Houvet, Email: 5s9ku.consent-[timestamp]@inbox.testmail.app |

---

## User Journey Overview

```
PHASE 1: Lead Capture (Admin or RM)
  └─ Create Close Corporation (Entity) lead with contact person details
       └─ Lead status: New

PHASE 2: Pre-Screening (Admin or RM)
  └─ Initiate Pre-Screening → answer 7 questions → Submit
       └─ Lead status: Converted
       └─ Opportunity auto-created (Draft, Entity type)
       └─ Account auto-created

PHASE 3: Opportunity Setup (RM — Fatima)
  └─ Edit opportunity → fill Entity Info (Entity Name, Reg Number, BEEE, Address, etc.)
  └─ Edit opportunity → fill Contact Person details
  └─ Edit opportunity → add Directors (with marital details)
  └─ Edit opportunity → add Signatories
  └─ Edit opportunity → fill Loan Info (Product + Amount + Purpose required)
       └─ Opportunity status: Draft

PHASE 4: Initiate Loan Application (RM — Fatima)
  └─ Click "Initiate Loan Application"
       └─ Opportunity status: Resolution Pending
       └─ Resolution emails sent to ALL directors

PHASE 4a: Sign Company Resolution (ALL Directors, via email)
  └─ For EACH director: retrieve resolution email → open URL → OTP → sign
  └─ ALL directors must sign before status progresses
       └─ Opportunity status: Consent Pending (after all sign)

PHASE 4b: Upload Entity Consent (Contact Person, via email)
  └─ Retrieve consent email from testmail.app API
  └─ Open consent URL from email
  └─ Request OTP → Retrieve OTP email → Submit OTP
  └─ Sign consent
       └─ Opportunity status: Verification In Progress
       └─ Workflow item created in Inbox

PHASE 5: Confirm Verification Outcomes (RM — Fatima, from Inbox)
  └─ Review verification details (CIPC Verification, Compliance, Signatories, Directors)
  └─ Click "Finalise Verification Outcomes"
       └─ Auto-advances to next step

PHASE 6: Complete Onboarding Checklist (RM — Fatima)
  └─ Fill pre-onboarding questions (9 items + conditionals)
  └─ Click "Submit"
       └─ Workflow: COMPLETED
       └─ Opportunity status: Complete
```

---

## Accounts Used

| Role | Username | Password | Used In |
|------|----------|----------|---------|
| System Administrator | admin | 123qwe | Phase 1, Phase 2, Phase 3 |
| RM (Relationship Manager) | fatima.abrahams@landbank.co.za | 123qwe | Phase 3–6 |

---

## PHASE 1: Lead Capture

### TC-01: Create Close Corporation (Entity) lead
- **Type:** Happy path
- **Login:** admin
- **URL:** {{BASE_URL}}/dynamic/LandBank.Crm/LBLead-table
- **Steps:**
  1. Navigate to Leads table via sidebar menu
  2. Click "New Lead"
  3. Fill all required fields (see input data)
  4. Click OK
- **Input data:**
  | Field | Value | Type | Required |
  |-------|-------|------|----------|
  | Owner | System Administrator (pre-filled) | Autocomplete | Yes |
  | Title | Mr | Dropdown | Yes |
  | First Name | Entity76374 (unique per run) | Text | Yes |
  | Last Name | Houvet | Text | Yes |
  | Mobile Number | 0712345678 | Text | Yes |
  | Email Address | 5s9ku.consent-[timestamp]@inbox.testmail.app | Text | Yes |
  | Client Type | Close Corporation (Entity) | Dropdown | Yes |
  | Province | Gauteng | Dropdown | Yes |
  | Preferred Communication | Email | Dropdown | Yes |
  | Lead Channel | Employee Referral | Dropdown | Yes |
- **Expected result:** Lead created with status "New"
- **Assertions:**
  - [x] Lead appears at top of Leads table
  - [x] Item count increments by 1
  - [x] Lead status: "New"
  - [x] All fields saved correctly
  - [x] Client Type shows "Close Corporation"

### Dropdown Values — Lead Creation
| Field | Options |
|-------|---------|
| Title | Unknown, Mr, Mrs, Ms, Dr, Prof |
| Client Type | Individual (Individual), Close Corporation (Entity), Sole Proprietor (Individual), Co-Corporation (Entity), Listed Company (Entity) |
| Province | Eastern Cape, Free State, Gauteng, KwaZulu-Natal, Limpopo, Mpumalanga, North West, Northern Cape, Western Cape |
| Preferred Communication | WhatsApp, Email, Call |
| Lead Channel | Advertisment, Cold Call, Employee Referral, External Referral, Online Store, Twitter, Facebook, Public Relations, Sales Email Alias, Seminar Partner |

---

## PHASE 2: Pre-Screening

### TC-02: Initiate Pre-Screening — all criteria pass
- **Type:** Happy path
- **Login:** admin (or RM)
- **URL:** {{BASE_URL}}/dynamic/LandBank.Crm/LBLead-details?id={leadId}
- **Steps:**
  1. Open the lead created in TC-01
  2. Verify header: "Houvet, Entity76374", Status: New
  3. Click "Initiate Pre-Screening"
  4. Answer all 7 questions with qualifying answers
  5. Tick confirmation checkbox
  6. Click "Submit"
- **Pre-Screening Answers:**
  | # | Question | Answer (Pass) |
  |---|----------|---------------|
  | 1 | Is the applicant a South African citizen? | Yes |
  | 2 | Is the farming land located in South Africa? | Yes |
  | 3 | Do the intended farming activities fall within the Land Bank mandate? | Yes |
  | 4 | Is the client blacklisted? | **No** |
  | 5 | Is the client currently under debt review? | **No** |
  | 6 | Is the client's current Country of Residence South Africa? | Yes |
  | 7 | Does the client currently have access to suitable land for farming activities? | Yes |
- **Expected result:** Pre-screening passes, opportunity and account auto-created
- **Assertions:**
  - [x] "Pre-assessment passed!" message
  - [x] "Opportunity created!" message
  - [x] Lead status → "Converted"
  - [x] Assessment → "Passed"
  - [x] "Converted To Opportunity" link appears
  - [x] "Converted To Account" link appears
  - [x] "Initiate Pre-Screening" button disappears

---

## PHASE 3: Opportunity Setup

### TC-03: Edit Entity Info — fill all mandatory fields
- **Type:** Happy path
- **Login:** admin or RM (Fatima)
- **URL:** {{BASE_URL}}/dynamic/LandBank.Crm/LBOpportunity-details?id={oppId}
- **Steps:**
  1. Navigate to opportunity (via "Converted To Opportunity" link or Opportunities table)
  2. Verify: Draft status, Entity type, Client Info section visible
  3. Click "Edit"
  4. Set Opportunity Owner
  5. Fill Entity Name
  6. Fill Company Registration Number
  7. Fill Years In Operation
  8. Select Entity Org Type
  9. Select BEEE Level
  10. Set Country Of Residence: South Africa
  11. Set Citizenship: South Africa
  12. Set Client Classification: Development
  13. Set Registered Address via Google Places
  14. Set Provincial Office
  15. **Leave** "Does the client have a resolution?" **unchecked** (checking requires uploading a signed resolution document — the resolution is handled via email in Phase 4a instead)
  16. Fill Contact Person fields (Title, Name, Surname, Email, Mobile)
  17. Switch to **Loan Info** tab → fill Product, Amount, Purpose (see TC-04 input data)
  18. Click **"Save"** once (single save for all tabs)
- **Input data:**
  | Field | Value | Type |
  |-------|-------|------|
  | Opportunity Owner | Fatima Abrahams | Dropdown |
  | Entity Name | Boxfusion (unique per run — e.g., Entity76374) | Text |
  | Company Registration Number | 2012/225386/07 | Text |
  | Years In Operation | 10 | Text (numeric) |
  | Entity Org Type | Close Corporation | Dropdown |
  | BEEE Level | Level 1 | Dropdown |
  | Country Of Residence | South Africa | Searchable dropdown |
  | Citizenship | South Africa | Searchable dropdown |
  | Client Classification | Development | Dropdown |
  | Registered Address | 100 Main Street, Marshalltown, Johannesburg, SA | Google Places |
  | Province | Gauteng | Pre-filled or Dropdown |
  | Region | Central Region | Auto-mapped |
  | Provincial Office | Provincial Office | Dropdown |
  | Does the client have a resolution? | **Unchecked** (requires document upload — resolution handled via email flow in TC-05r) | Checkbox |
  | Contact Person Title | Mr | Dropdown |
  | Contact Person Name | Ian | Text |
  | Contact Person Surname | Houvet | Text |
  | Contact Person Email | 5s9ku.consent-[timestamp]@inbox.testmail.app | Text |
  | Contact Person Mobile | 0712345678 | Text |
- **Expected result:** "Data saved successfully!"
- **Assertions:**
  - [x] All entity fields saved and displayed correctly
  - [x] Province → Region auto-mapping works (Gauteng → Central Region)
  - [x] Google Places auto-fills registered address
  - [x] Contact Person fields saved correctly
  - [x] Application Type shows "Entity" (not "Personal")
  - [x] "Does the client have a resolution?" checkbox is unchecked (resolution handled via email flow)

### TC-03a: Add Directors
- **Type:** Happy path
- **Login:** admin or RM (Fatima)
- **Steps:**
  1. Click "Edit" on opportunity (if not already in edit mode)
  2. Navigate to Directors section
  3. Add Director 1: Ian Houvet (Married in Community of Property)
  4. Add Director 2: Chamaine Houvet (Single)
  5. Add Director 3: Xolile Ndlangana (Single)
  6. Click "Save"
- **Director 1 Input Data:**
  | Field | Value | Type |
  |-------|-------|------|
  | First Name | Ian | Text |
  | Last Name | Houvet | Text |
  | ID Number | 7708206169188 | Text |
  | Email | 5s9ku.consent-[timestamp]@inbox.testmail.app | Text |
  | Mobile | 0712345678 | Text |
  | Citizenship | South Africa | Searchable dropdown |
  | Country Of Residence | South Africa | Searchable dropdown |
  | Country Of Origin | South Africa | Searchable dropdown |
  | Marital Status | Married | Dropdown |
  | Marital Regime | Married in Community of Property | Dropdown (conditional — appears when Married) |
  | Spouse First Name | Chamaine | Text (conditional — appears for Community of Property) |
  | Spouse Last Name | Houvet | Text (conditional) |
  | Spouse ID Number | 7304190225085 | Text (conditional) |
- **Director 2 Input Data:**
  | Field | Value | Type |
  |-------|-------|------|
  | First Name | Chamaine | Text |
  | Last Name | Houvet | Text |
  | ID Number | 7304190225085 | Text |
  | Email | 5s9ku.dir2-[timestamp]@inbox.testmail.app | Text |
  | Mobile | 0712345679 | Text |
  | Citizenship | South Africa | Searchable dropdown |
  | Country Of Residence | South Africa | Searchable dropdown |
  | Country Of Origin | South Africa | Searchable dropdown |
  | Marital Status | Single | Dropdown |
- **Director 3 Input Data:**
  | Field | Value | Type |
  |-------|-------|------|
  | First Name | Xolile | Text |
  | Last Name | Ndlangana | Text |
  | ID Number | 6311115651080 | Text |
  | Email | 5s9ku.dir3-[timestamp]@inbox.testmail.app | Text |
  | Mobile | 0712345680 | Text |
  | Citizenship | South Africa | Searchable dropdown |
  | Country Of Residence | South Africa | Searchable dropdown |
  | Country Of Origin | South Africa | Searchable dropdown |
  | Marital Status | Single | Dropdown |

> **IMPORTANT:** ALL director emails MUST use testmail.app addresses (unique tag per director per run). The resolution flow sends emails to every director, and all must sign. Using non-testmail addresses (e.g. @boxfusion.io) will block the resolution step since those inboxes can't be queried programmatically.
- **Expected result:** "Data saved successfully!" — 3 directors listed
- **Assertions:**
  - [x] Director 1 (Ian Houvet) saved with Married status and spouse details
  - [x] Director 2 (Chamaine Houvet) saved with Single status
  - [x] Director 3 (Xolile Ndlangana) saved with Single status
  - [x] Marital Regime field only appears when Marital Status = Married
  - [x] Spouse fields only appear when Marital Regime = Married in Community of Property
  - [x] All 3 directors visible in Directors list

### TC-03b: Add Signatories
- **Type:** Happy path
- **Login:** admin or RM (Fatima)
- **Steps:**
  1. Click "Edit" on opportunity (if not already in edit mode)
  2. Navigate to Signatories section
  3. Add Signatory: Ian Houvet
  4. Click "Save"
- **Signatory Input Data:**
  | Field | Value | Type |
  |-------|-------|------|
  | First Name | Ian | Text |
  | Last Name | Houvet | Text |
  | ID Number | 7708206169188 | Text |
  | Email | 5s9ku.consent-[timestamp]@inbox.testmail.app | Text |
  | Mobile | 0712345678 | Text |
- **Expected result:** "Data saved successfully!" — 1 signatory listed
- **Assertions:**
  - [x] Signatory (Ian Houvet) saved with correct details
  - [x] Signatory visible in Signatories list

### Dropdown Values — Entity Info
| Field | Options |
|-------|---------|
| Opportunity Owner | Awelani Matodzi, Bonolo Lebelo, Fatima Abrahams, Fatima CBA, Francois du Plessis, Jacob Mbonani, James Smith, Molatelo Moshia |
| Client Classification | Development, Commercial |
| Marital Status (Directors) | Single, Married, Divorced, Widowed, Separated, Domestic Partnership |
| Marital Regime (Directors) | Married in Community of Property, Married out of Community with Accrual, Married out of Community without Accrual |
| Country dropdowns | Searchable — full country list, type to filter |

### TC-04: Fill Loan Info — Products, Amount, Purpose (required for workflow)
- **Type:** Happy path
- **Login:** RM (Fatima)
- **Steps:**
  1. Click "Edit" on opportunity
  2. Click "Loan Info" tab
  3. Click ellipsis (...) on Products field → entity picker opens
  4. Double-click a product to select it
  5. Enter Business Summary
  6. Enter Requested Amount (must be > 0)
  7. Select Existing Relationship with Bank
  8. Select Sources Of Income
  9. In Loan Purpose table: select Purpose, enter Amount, click add (+)
  10. Click "Save"
- **Input data:**
  | Field | Value | Type |
  |-------|-------|------|
  | Products | R MT Loans (CB&T) | Entity picker (double-click to select) |
  | Business Summary | Farming operations in Gauteng region | Textarea |
  | Requested Amount | 500000 | Text (numeric) |
  | Existing Relationship with Bank | None | Dropdown |
  | Sources Of Income | Farming income | Dropdown |
  | Loan Purpose → Purpose | Purchase Of Livestock | Dropdown |
  | Loan Purpose → Amount | 500000 | Text (numeric) |
- **Expected result:** "Data saved successfully!", Amount shows 500000 in header
- **Assertions:**
  - [x] Product selected via entity picker dialog
  - [x] Business Summary saved
  - [x] Requested Amount saved and displayed in header
  - [x] Loan Purpose row added to table
  - [x] "Data saved successfully!" confirmation

### Dropdown Values — Loan Info
| Field | Options |
|-------|---------|
| Existing Relationship with Bank | Existing Client, None |
| Sources Of Income | Salary, Farming income, Business income, Rental income, Pension income, Dividends |
| Loan Purpose | Improvements To Farming Property, Purchase Of Livestock, Financing Agri-Debt, Establishment Costs, Purchase Of Movable Assets, Purchase Of Production Inputs For Crops, Purchase Of Production Inputs For Livestock, Production loan re-advance, Revolving facility review, Other (Please specify) |

### Products Available (Entity Picker)
| Name | Division |
|------|----------|
| R MT Loans | CB&T |
| C LT Loans | LDFU |
| AEF | CB&T |
| REM ISF | CB&T |
| Grants | CB&T |
| Liq Fac | CB & SI |
| C MT Loans | CB & SI |
| C Guarant. | CD&T |
| Equities | CB&T |
| R LT Loans | CB&T |
| (+ 7 more) | — |

---

## PHASE 4: Initiate Loan Application

### TC-05: Initiate Loan Application
- **Type:** Happy path
- **Login:** RM (Fatima)
- **Prereqs:** Entity Info filled, Directors added, Signatories added, Product selected, Requested Amount > 0
- **Steps:**
  1. On opportunity page, click "Initiate Loan Application"
- **Expected result:** Workflow starts, status changes to Resolution Pending, resolution emails sent to ALL directors
- **Assertions:**
  - [ ] Toast: "Loan Application submitted successfully"
  - [ ] Opportunity status → **"Resolution Pending"** (Entity flow — NOT "Consent Pending")
  - [ ] "Initiate Loan Application" button disappears
  - [ ] Resolution emails sent to all 3 director email addresses

### TC-05a: Initiate without Requested Amount (negative)
- **Type:** Negative
- **Steps:**
  1. With Requested Amount = 0, click "Initiate Loan Application"
- **Expected result:** Error blocks initiation
- **Assertions:**
  - [x] Error: "Cannot initiate workflow: requested amount must be greater than zero."
  - [x] Status remains "Draft"

### TC-05b: Initiate without Product (negative)
- **Type:** Negative
- **Steps:**
  1. With no Product selected (but Amount > 0), click "Initiate Loan Application"
- **Expected result:** Error blocks initiation
- **Assertions:**
  - [x] Error: "Cannot initiate workflow: at least one product is required."
  - [x] Status remains "Draft"

### TC-05r: Sign Company Resolution (ALL Directors)
- **Type:** Happy path
- **Login:** Not needed (resolution page is public link from email)
- **Steps — repeat for EACH director (Ian, Chamaine, Xolile):**
  1. Call testmail.app API with the director's tag to retrieve resolution email
     - Subject: "Action Required: Company Resolution Needed for Loan Application"
  2. Extract resolution URL from email body (href matching `entity-application-resolution-approval`)
  3. Navigate to resolution URL in browser
  4. Verify resolution page loads:
     - Company Name, Registration Number
     - Directors table (all 3 listed)
     - Nominated Signatories table
  5. Click "Request OTP"
  6. Verify toast: "The one-time-password (OTP) has been sent"
  7. Call testmail.app API with director's tag + timestamp_from to get OTP email
  8. Extract OTP: `Your One-Time-Pin is (\d+)`
  9. Fill OTP into input field
  10. Click "Submit OTP and Sign Resolution"
  11. Click "Submit" in confirmation dialog
  12. Verify success: "Resolution signed successfully!"
  13. After ALL 3 directors have signed:
     - Navigate back to opportunity page
     - Verify status changed to **"Consent Pending"**
- **Director email tags (for testmail.app API calls):**
  | Director | Testmail tag | API tag parameter |
  |----------|-------------|-------------------|
  | Ian Houvet | consent-[timestamp] | consent-[timestamp] |
  | Chamaine Houvet | dir2-[timestamp] | dir2-[timestamp] |
  | Xolile Ndlangana | dir3-[timestamp] | dir3-[timestamp] |
- **Expected result:** All 3 resolutions signed, status progresses to "Consent Pending"
- **Assertions:**
  - [ ] Resolution email received for each director
  - [ ] Resolution URL extracted from each email
  - [ ] Resolution page shows correct company details and all directors
  - [ ] OTP flow works for each director
  - [ ] Success: "Resolution signed successfully!" for each director
  - [ ] After all 3 sign: Opportunity status → "Consent Pending"

### TC-05c: Upload Entity Consent
- **Type:** Happy path
- **Login:** Not needed (consent page is public link from email)
- **Prereqs:** TC-05r complete — all directors have signed the resolution, status is "Consent Pending"
- **Steps:**
  1. Call testmail.app API to retrieve consent email (tag from contact person email)
     - Subject: "Action Required: Provide Consent to Process Your Loan Application"
  2. Extract consent URL from email body (href matching `individual-application-consent`)
  3. Navigate to consent URL in browser
  4. Verify consent page loads (consent form heading visible)
  5. Click "Request OTP" button
  6. Verify toast: "The one-time-password (OTP) has been sent"
  7. Call testmail.app API again with timestamp_from to get OTP email
  8. Extract OTP from body using regex: `Your One-Time-Pin is (\d+)`
  9. Fill OTP into input field
  10. Click "Submit OTP and Sign Consent"
  11. Click confirmation button in dialog
  12. Verify success toast: "Thank you for providing consent"
  13. Navigate back to opportunity page
  14. Verify status changed to "Verification In Progress"
- **Expected result:** Consent signed, status changes to "Verification In Progress"
- **Assertions:**
  - [ ] Consent email received via testmail.app API
  - [ ] Consent URL extracted from email
  - [ ] Consent page loaded
  - [ ] OTP requested successfully (toast shown)
  - [ ] OTP email received via testmail.app API
  - [ ] OTP extracted from email body
  - [ ] OTP submitted and consent signed
  - [ ] Success toast: "Thank you for providing consent"
  - [ ] Opportunity status: Verification In Progress

### Testmail.app API (for consent/OTP emails)
| Field | Value |
|-------|-------|
| Namespace | 5s9ku |
| API Key | b300bfdf-3e55-4478-9e27-072849073ed4 |
| Inbox domain | @inbox.testmail.app |
| Email format | 5s9ku.{tag}@inbox.testmail.app |
| API endpoint | GET https://api.testmail.app/api/json?apikey={key}&namespace={ns}&tag={tag}&livequery=true&timeout=60000 |

---

## PHASE 5: Confirm Verification Outcomes

### TC-06: Review and finalise entity verification
- **Type:** Happy path
- **Login:** RM (Fatima)
- **URL:** {{BASE_URL}}/dynamic/Shesha.Workflow/workflows-inbox
- **Steps:**
  1. Navigate to Inbox via sidebar menu
  2. Find the workflow item (Ref No: LA2026/XXXX, Action: "Confirm verification outcomes")
  3. Click the search icon to open it
  4. Review the loan application details (Entity Info, Loan Info, Farms — read-only)
  5. **Review Entity CIPC Verification:**
     a. In "Entity Verifications" section, click "Awaiting Review" for the entity
     b. Record CIPC Verification details (Status, Submitted vs Returned data)
     c. If CIPC status is "Awaiting Review" → make a Review Decision (Approve/Reject) before proceeding
     d. Close the entity verification dialog
     e. Verify the entity status badge changed from "Awaiting Review"
  6. **For EACH director in "Individual Verifications" section**, perform steps 7–12:
  7. Click "Awaiting Review" for the director
  8. **Overview tab** — record and assert:
     - ID Status (expect: Completed or Awaiting Review)
     - Photo Verification Status
     - KYC Status
     - Compliance Verification
  9. **ID Verification tab** — record and assert:
     - Status + Date Submitted
     - Submitted data: First Name, Last Name, ID Number
     - Returned data: First Name, Last Name, ID Number, DOB, Gender
     - Assert each check:
       - [ ] Name Match: Passed/Failed/Requires Review
       - [ ] ID Match: Passed/Failed
       - [ ] Death Check: Passed/Failed
       - [ ] Outcome: Passed/Failed/TBD
     - If Outcome is not Passed or Name Match is not Passed → must make a Review Decision (Approve/Reject) before proceeding
     - Face Photo: present or "No image available"
  10. **KYC Verification tab** — record and assert:
      - Status + Date Submitted
      - Submitted data: ID Number
      - Returned data: ID Number, First Name, Address, Cell Number, Employer, etc.
      - Assert:
        - [ ] First Name Match Status: Passed/Failed
        - [ ] Outcome: Passed/Failed
      - If needs review → select KYC Verification First Name Review Decision before proceeding
  11. Close dialog for this director
  12. Verify their status badge changed from "Awaiting Review" to something else (Completed/Reviewed)
  13. **Before Finalise:** Verify there are ZERO "Awaiting Review" buttons remaining (entity + all directors)
  14. Only then click "Finalise Verification Outcomes"

- **Entity Verification:**
  - Boxfusion (Reg: 2012/225386/07) — CIPC Verification

- **Individual Verifications (3 directors):**
  - Ian Houvet (7708206169188)
  - Chamaine Houvet (7304190225085)
  - Xolile Ndlangana (6311115651080)

- **Expected result:** Workflow advances to next step (Complete Onboarding Checklist)
- **Assertions:**
  - [ ] Inbox shows workflow item with "Confirm verification outcomes" action
  - [ ] Workflow page shows loan application details (read-only)
  - [ ] "Entity Verifications" section visible (not "Individual Verifications")
  - [ ] Entity CIPC verification reviewed (see report format below)
  - [ ] Ian Houvet verification reviewed (ID + KYC)
  - [ ] Chamaine Houvet verification reviewed (ID + KYC)
  - [ ] Xolile Ndlangana verification reviewed (ID + KYC)
  - [ ] Zero "Awaiting Review" buttons remaining before Finalise
  - [ ] "Finalise Verification Outcomes" button advances workflow
  - [ ] Auto-redirects to "Complete Onboarding Checklist" step

#### Report Format for TC-06

For the entity, record CIPC verification using this format:

```
### Entity: Boxfusion (2012/225386/07)

**CIPC Verification:**
- Status: Completed / Awaiting Review
- Reason for Failure: (if any, e.g., Company name mismatch)
- Submitted: Reg Number 2012/225386/07, Company Name (from entity)
- Returned: Reg Number K2012/225386/07, Company Name BOXFUSION (PTY)LTD
- Business Status: In Business
- Company Type: Private Company
- VAT Number: 4760252900
- Company Age: 13 Years 3 Months
- Registration Date: 2012-12-19
- Physical Address: International Business Gateway, New Road Midridge Park, Midrand, Gauteng, 1684
- Review Decision: Approve / Reject / Not required
```

For each director, record verification outcomes using this format:

```
### Individual: Ian Houvet (7708206169188)

**Overview:**
- ID Status: Completed / Awaiting Review
- Photo Verification Status: Completed / Awaiting Review
- KYC Status: Completed / Initiated / Awaiting Review
- Compliance Verification: Completed / Awaiting Review

**ID Verification:**
- Status: Completed | Date: DD/MM/YYYY
- Submitted: Ian Houvet, 7708206169188
- Returned: IAN HOUVET, 7708206169188, DOB 20/08/1977, Male
- Name Match: [x] Passed
- ID Match: [x] Passed
- Death Check: [x] Passed
- Outcome: [x] Passed
- Face Photo: Present / No image available
- Review Decision: Not required (all passed) / Approve / Reject

**KYC Verification:**
- Status: Completed | Date: DD/MM/YYYY
- Submitted: 7708206169188
- Returned: IAN, Address: 34 VINCENT AVE..., Cell: 0761598891, Employer: BOXFUSION
- First Name Match: [x] Passed
- Outcome: [x] Passed
- Review Decision: Not required (all passed) / Approve / Reject
```

Repeat the above block for each director:
- Ian Houvet (7708206169188)
- Chamaine Houvet (7304190225085)
- Xolile Ndlangana (6311115651080)

### Alternative Actions Available (not tested)
- **Flag As High Risk** — routes to different workflow path (to be tested)

### Inbox Table Columns
| Column | Description |
|--------|-------------|
| Ref No | Loan application reference (e.g., LA2026/0938) |
| Initiator | User who triggered the workflow |
| Type | "Loan Application Workflow" |
| Name | (empty) |
| Action Required | Current step name |
| Received Date | Date/time |
| Status | In Progress / Completed |

---

## PHASE 6: Complete Onboarding Checklist

### TC-07: Fill and submit pre-onboarding checklist
- **Type:** Happy path
- **Login:** RM (Fatima)
- **Steps:**
  1. On the "Complete Onboarding Checklist" workflow page
  2. Review loan application details (read-only)
  3. Select Years Of Farming Experience
  4. Check all applicable checklist items
  5. Click "Submit"
- **Input data:**
  | Question | Value | Type |
  |----------|-------|------|
  | Years Of Farming Experience | 4 to 6 Years | Dropdown |
  | Does this operation require Water Use Rights? | Yes | Checkbox |
  | Support with applying for water rights required? | Yes | Checkbox (conditional — only appears if Water Use Rights = Yes) |
  | Business Plan Development Support required? | Yes | Checkbox |
  | Is there access to working Equipment and Mechanization? | Yes | Checkbox |
  | Does the client have a Valid Tax Clearance certificate? | Yes | Checkbox |
  | Does the client have access to established markets? | Yes | Checkbox |
  | Formal Financial Records or Statements maintained? | Yes | Checkbox |
  | Does the client have an actively engaged Mentor? | Yes | Checkbox |
  | Is the client Compliant with all applicable Labor Laws? | Yes | Checkbox |
- **Expected result:** Checklist saved, workflow completes
- **Assertions:**
  - [x] "Checklist saved successfully." message
  - [x] Workflow status → "COMPLETED"
  - [x] "Requested action is not available" shown (no more steps)
  - [x] Opportunity status → "Complete"

### Dropdown Values — Onboarding Checklist
| Field | Options |
|-------|---------|
| Years Of Farming Experience | Up to 2 Years, 2 to 4 Years, 4 to 6 Years, 6 to 10 Years, More than 10 Years |

### Conditional Fields
| Trigger | Condition | Revealed Field |
|---------|-----------|---------------|
| Does this operation require Water Use Rights? | Checked | "Support with applying for water rights required?" |

---

## Status Lifecycle Summary

| Phase | Action | Opportunity Status | Workflow Status |
|-------|--------|-------------------|-----------------|
| Phase 1 | Lead created | — | — |
| Phase 2 | Pre-screening passed | Draft | — |
| Phase 3 | Entity Info + Directors + Signatories + Loan Info filled | Draft | — |
| Phase 4 | Initiate Loan Application | **Resolution Pending** | — |
| Phase 4a | ALL directors sign resolution | **Consent Pending** | — |
| Phase 4b | Contact Person signs consent | Verification In Progress | In Progress |
| Phase 5 | Finalise Verification Outcomes | Verification In Progress | In Progress (next step) |
| Phase 6 | Submit Onboarding Checklist | **Complete** | **Completed** |

---

## Workflow Prerequisites

The following must be completed before "Initiate Loan Application" is enabled:
1. Opportunity Owner must be set
2. At least one **Product** must be selected (via entity picker)
3. **Requested Amount** must be greater than zero
4. Entity Info mandatory fields: Entity Name, Company Registration Number, Contact Person Name, Surname, Email, Mobile, Client Classification
5. ALL director emails must use testmail.app addresses (required for resolution signing)

---

## Key Differences from Personal Loan Application

| Aspect | Personal | Entity (Close Corporation) |
|--------|----------|---------------------------|
| Client Type | Individual | Close Corporation (Entity) |
| Application Type | Personal | Entity |
| Client Name fields | Client Name, Surname | Entity Name, Company Registration Number |
| Address | Residential Address | Registered Address |
| Country fields | Country Of Residence, Citizenship, Country Of Origin | Country Of Residence, Citizenship (no Country Of Origin at entity level) |
| Extra entity fields | — | Years In Operation, Entity Org Type, BEEE Level, Resolution checkbox |
| Contact Person | N/A (client is the person) | Contact Person Title, Name, Surname, Email, Mobile |
| Directors | N/A | Multiple directors with full details + marital info + spouse |
| Signatories | N/A | First Name, Last Name, ID Number, Email, Mobile |
| Post-initiate flow | Consent Pending → consent → Verification In Progress | Resolution Pending → (all directors sign) → Consent Pending → consent → Verification In Progress |
| Verification (TC-06) | Individual Verifications (ID, Photo, KYC, Compliance) | Entity Verifications (CIPC Verification, Compliance, Signatories, Directors) |
| Marital fields | Marital Status on client | Marital Status + Marital Regime on each director |
| Director emails | N/A | ALL must use testmail.app for automated resolution signing |

---

## RM (Fatima) Role Observations

| Feature | Available | Notes |
|---------|-----------|-------|
| Dashboard | Yes | "My Dashboard" — 0 stats initially |
| Inbox | Yes | Shows workflow items assigned to user |
| Leads | Yes | Can create and view |
| Opportunities | Yes | Can edit, initiate workflow |
| Crm | Yes | Sub-menu |
| Workflows | Yes | Sub-menu |
| Cases | **No** | Not visible |
| Reports | **No** | Not visible |
| Service Management | **No** | Not visible |
| Administration | **No** | Not visible |
| Configurations | **No** | Not visible |
| Compliance tab (on opportunity) | **No** | Not visible for RM role |

---

## Rules

- Lead must pass all 7 pre-screening criteria to convert to opportunity
- Opportunity is auto-created on pass — cannot be created manually
- Contact Person fields pre-populate from lead data (First Name, Last Name, Email, Mobile)
- Province → Region mapping is automatic (Gauteng → Central Region)
- Entity opportunities have Directors section with Marital Status AND Marital Regime
- Marital Regime only appears when Director's Marital Status = Married
- Spouse fields only appear when Marital Regime = Married in Community of Property
- Directors have Country Of Origin field (entity level does not)
- Workflow requires Products + Amount > 0 before initiation
- Initiation triggers resolution flow first (status: Resolution Pending → resolution emails sent to ALL directors)
- ALL directors must sign the resolution before status progresses to Consent Pending
- After all resolutions signed, consent email is sent to the Contact Person email address
- ALL director emails MUST use testmail.app addresses for automated resolution signing
- Entity verification uses CIPC check (not ID/KYC like Personal)
- CIPC may return "Awaiting Review" with company name mismatch — this does not block finalization
- Verification step auto-advances after "Finalise Verification Outcomes"
- Onboarding checklist has conditional fields (Water Use Rights → Support with water rights)
- After workflow completes, opportunity status is "Complete" and no further actions available

---

## Test Execution Record

| TC | Description | Result | Date | Tester |
|----|-------------|--------|------|--------|
| TC-01 | Create Close Corporation (Entity) lead | Pass | 2026-03-18 | admin |
| TC-02 | Pre-Screening — all pass | Pass | 2026-03-18 | admin |
| TC-03 | Edit Entity Info + Contact Person | Pass | 2026-03-18 | admin |
| TC-03a | Add Directors (3) | Pass | 2026-03-18 | admin |
| TC-03b | Add Signatories (1) | Pass | 2026-03-18 | admin |
| TC-04 | Fill Loan Info | Pass | 2026-03-18 | Fatima Abrahams |
| TC-05 | Initiate Loan Application | Pass | 2026-03-18 | Fatima Abrahams |
| TC-05a | Initiate without Amount (negative) | Pass | 2026-03-18 | Fatima Abrahams |
| TC-05b | Initiate without Product (negative) | Pass | 2026-03-18 | Fatima Abrahams |
| TC-05c | Upload Entity Consent | — | — | — |
| TC-06 | Confirm Entity Verification Outcomes | Pass | 2026-03-18 | Fatima Abrahams |
| TC-07 | Complete Onboarding Checklist | Pass | 2026-03-18 | Fatima Abrahams |

**Lead:** Entity76374 Houvet (ID: 5b7040cf-9d81-41f2-8c57-da7f58d50ce7)
**Opportunity:** Entity76374 Houvet (ID: 426146be-755f-48c7-8fdb-64c2beab46ed)
**Account:** Entity76374 Houvet (ID: 1ce57116-cd06-4ba4-8718-ac2c21b95107)
**Workflow Ref:** LA2026/0938
**Lead Ref:** LD-2026-000730

---

## Still To Test

1. **Negative pre-screening** — what happens when a disqualifying answer is given?
2. **Flag As High Risk** — alternative path at verification step
3. **Incomplete onboarding checklist** — can it be submitted with unchecked items?
4. **CIPC verification failure** — what if CIPC returns a hard failure (not just mismatch)?
5. **Multiple products** — can more than one product be selected?
6. **Multiple loan purposes** — add several rows with different purposes
7. **Edit after workflow start** — can Entity Info be edited while in Verification In Progress?
8. **Director removal** — can directors be removed after adding?
9. **Director without spouse** — Married but NOT in Community of Property (no spouse fields)
10. **Multiple signatories** — add more than one signatory
11. **Resolution unchecked** — what happens if "Does the client have a resolution?" is not checked?
12. **Farm addition** — add farm before initiating workflow
