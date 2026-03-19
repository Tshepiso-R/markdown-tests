# Test Plan: End-to-End Personal Loan Application

## Meta
| Field        | Value                                                              |
|-------------|--------------------------------------------------------------------|
| Module      | Full Journey — Lead → Opportunity → Workflow → Complete            |
| URL         | {{BASE_URL}} = landbankcrm-adminportal-qa.shesha.app               |
| Prereqs     | Admin account for lead creation; RM account (Fatima) for workflow   |
| Last tested | 2026-03-17                                                         |
| Status      | Pass                                                               |
| Test Data   | Ian Houvet, ID: 7708206169188, Email: 5s9ku.consent-[timestamp]@inbox.testmail.app |

---

## User Journey Overview

```
PHASE 1: Lead Capture (Admin or RM)
  └─ Create Individual lead with client details
       └─ Lead status: New

PHASE 2: Pre-Screening (Admin or RM)
  └─ Initiate Pre-Screening → answer 7 questions → Submit
       └─ Lead status: Converted
       └─ Opportunity auto-created (Draft)
       └─ Account auto-created

PHASE 3: Opportunity Setup (RM — Fatima)
  └─ Edit opportunity → fill Client Info (all fields except marital regime)
  └─ Edit opportunity → fill Loan Info (Product + Amount + Purpose required)
       └─ Opportunity status: Draft

PHASE 4: Initiate Loan Application (RM — Fatima)
  └─ Uncheck Auto Verify checkbox
  └─ Click "Initiate Loan Application"
       └─ Opportunity status: Consent Pending
       └─ Consent email sent to applicant

PHASE 4.5: Upload Individual Consent (Applicant, via email)
  └─ Retrieve consent email from testmail.app API
  └─ Open consent URL from email
  └─ Request OTP → Retrieve OTP email → Submit OTP
  └─ Sign consent
       └─ Opportunity status: Verification In Progress
       └─ Workflow item created in Inbox

PHASE 5: Confirm Verification Outcomes (RM — Fatima, from Inbox)
  └─ Review verification details (ID, Photo, KYC, Compliance)
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

### TC-01: Create Individual lead
- **Type:** Happy path
- **Login:** admin
- **URL:** {{BASE_URL}}/dynamic/LandBank.Crm/LBLead-table
- **Steps:**
  1. Navigate to Leads table
  2. Click "New Lead"
  3. Fill all required fields (see input data)
  4. Click OK
- **Input data:**
  | Field | Value | Type | Required |
  |-------|-------|------|----------|
  | Owner | System Administrator (pre-filled) | Autocomplete | Yes |
  | Title | Mr | Dropdown | Yes |
  | First Name | IanH33468 (unique per run) | Text | Yes |
  | Last Name | Houvet | Text | Yes |
  | Mobile Number | 0712345678 | Text | Yes |
  | Email Address | 5s9ku.consent-[timestamp]@inbox.testmail.app | Text | Yes |
  | Client Type | Individual (Individual) | Dropdown | Yes |
  | Province | Gauteng | Dropdown | Yes |
  | Preferred Communication | Email | Dropdown | Yes |
  | Lead Channel | Employee Referral | Dropdown | Yes |
- **Expected result:** Lead created with status "New"
- **Assertions:**
  - [x] Lead appears at top of Leads table
  - [x] Item count increments by 1
  - [x] Lead status: "New"
  - [x] All fields saved correctly

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
  2. Verify header: "Houvet, IanH33468", Status: New
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

### TC-03: Edit Client Info — fill all mandatory fields except marital regime
- **Type:** Happy path
- **Login:** admin or RM (Fatima)
- **URL:** {{BASE_URL}}/dynamic/LandBank.Crm/LBOpportunity-details?id={oppId}
- **Steps:**
  1. Navigate to opportunity (via "Converted To Opportunity" link or Opportunities table)
  2. Verify: Draft status, Personal type, Client Info pre-populated from lead
  3. Click "Edit"
  4. Set Opportunity Owner
  5. Update Client Name from unique lead name to "Ian"
  6. Enter Client ID Number: 7708206169188
  7. Set Country Of Residence, Citizenship, Country Of Origin: South Africa
  8. Set Client Classification: Development
  9. Set Residential Address via Google Places
  10. Set Provincial Office
  11. Set Marital Status: Single
  12. **Leave Marital Regime empty** (intentional)
  13. Click "Save"
- **Input data:**
  | Field | Value | Source |
  |-------|-------|--------|
  | Opportunity Owner | Fatima Abrahams | Dropdown |
  | Client ID Number | 7708206169188 | Manual entry |
  | Client Name | Ian | Edit (was unique lead name) |
  | Client Surname | Houvet | Pre-filled |
  | Email Address | 5s9ku.consent-[timestamp]@inbox.testmail.app | Pre-filled |
  | Mobile Number | 0712345678 | Pre-filled |
  | Client Title | Mr | Pre-filled |
  | Preferred Communication | Email | Pre-filled |
  | Country Of Residence | South Africa | Searchable dropdown |
  | Citizenship | South Africa | Searchable dropdown |
  | Country Of Origin | South Africa | Searchable dropdown |
  | Client Classification | Development | Dropdown |
  | Residential Address | 100 Main Street, Marshalltown, Johannesburg, SA | Google Places |
  | Province | Gauteng | Pre-filled |
  | Region | Central Region | Auto-mapped |
  | Provincial Office | Provincial Office | Dropdown |
  | Marital Status | Single | Dropdown |
  | Marital Regime | (empty — intentional) | — |
- **Expected result:** "Data saved successfully!"
- **Assertions:**
  - [x] All fields saved and displayed correctly
  - [x] Province → Region auto-mapping works (Gauteng → Central Region)
  - [x] Google Places auto-fills address
  - [x] Marital Regime left empty without error

### Dropdown Values — Client Info
| Field | Options |
|-------|---------|
| Opportunity Owner | Awelani Matodzi, Bonolo Lebelo, Fatima Abrahams, Fatima CBA, Francois du Plessis, Jacob Mbonani, James Smith, Molatelo Moshia |
| Client Classification | Development, Commercial |
| Marital Status | Single, Married, Divorced, Widowed, Separated, Domestic Partnership |
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
- **Prereqs:** Client Info filled, Product selected, Requested Amount > 0, Auto Verify unchecked
- **Steps:**
  1. On opportunity page, click "Edit"
  2. Uncheck the "Auto Verify" checkbox
  3. Click "Save"
  4. Click "Initiate Loan Application"
- **Expected result:** Workflow starts, status changes to Consent Pending, consent email sent to applicant
- **Assertions:**
  - [ ] "Loan Application submitted successfully" message
  - [ ] Opportunity status → "Consent Pending"
  - [ ] "Initiate Loan Application" button disappears

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

### TC-05c: Upload Individual Consent
- **Type:** Happy path
- **Login:** Not needed (consent page is public link from email)
- **Steps:**
  1. Call testmail.app API to retrieve consent email (tag from lead email)
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

### TC-06: Review and finalise verification
- **Type:** Happy path
- **Login:** RM (Fatima)
- **URL:** {{BASE_URL}}/dynamic/Shesha.Workflow/workflows-inbox
- **Steps:**
  1. Navigate to Inbox
  2. Find the workflow item (Ref No: LA2026/XXXX, Action: "Confirm verification outcomes")
  3. Click the search icon to open it
  4. Review the loan application details (Client Info, Loan Info, Farms — read-only)
  5. In "Individual Verifications" section, click "Awaiting Review" button
  6. Review verification statuses in the dialog (Overview, ID Verification, KYC Verification tabs)
  7. Close the dialog
  8. Click "Finalise Verification Outcomes"
- **Verification Details Observed:**
  | Verification | Status |
  |-------------|--------|
  | ID Status | Completed |
  | Photo Verification Status | Awaiting Review |
  | KYC Status | Initiated |
  | Compliance Verification | Completed |
- **Expected result:** Workflow advances to next step (Complete Onboarding Checklist)
- **Assertions:**
  - [x] Inbox shows workflow item with "Confirm verification outcomes" action
  - [x] Workflow page shows loan application details (read-only)
  - [x] "Individual Verifications" section shows applicant: Ian Houvet
  - [x] "Awaiting Review" button opens verification detail dialog
  - [x] Verification dialog has Overview, ID Verification, KYC Verification tabs
  - [x] "Finalise Verification Outcomes" button advances workflow
  - [x] Auto-redirects to "Complete Onboarding Checklist" step

### Alternative Actions Available (not tested)
- **Flag As High Risk** — routes to different workflow path (to be tested)

### Inbox Table Columns
| Column | Description |
|--------|-------------|
| Ref No | Loan application reference (e.g., LA2026/0882) |
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
| Phase 3 | Client Info + Loan Info filled | Draft | — |
| Phase 4 | Initiate Loan Application | Consent Pending | — |
| Phase 4.5 | Upload Individual Consent | Verification In Progress | In Progress |
| Phase 5 | Finalise Verification Outcomes | Verification In Progress | In Progress (next step) |
| Phase 6 | Submit Onboarding Checklist | **Complete** | **Completed** |

---

## Workflow Prerequisites

The following must be completed before "Initiate Loan Application" is enabled:
1. Opportunity Owner must be set
2. At least one **Product** must be selected (via entity picker)
3. **Requested Amount** must be greater than zero
4. Client Info mandatory fields: Client Name, Surname, Email, Mobile, Preferred Communication, Client Classification
5. **Auto Verify** must be unchecked (to trigger consent flow instead of auto-verification)

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
- Client Info fields pre-populate from lead data
- Province → Region mapping is automatic (Gauteng → Central Region)
- Individual opportunities have Marital Status (not Marital Regime — that's Entity/Director only)
- Workflow requires Products + Amount > 0 before initiation
- Verification step auto-advances after "Finalise Verification Outcomes"
- Onboarding checklist has conditional fields (Water Use Rights → Support with water rights)
- After workflow completes, opportunity status is "Complete" and no further actions available

---

## Test Execution Record

| TC | Description | Result | Date | Tester |
|----|-------------|--------|------|--------|
| TC-01 | Create Individual lead | Pass | 2026-03-17 | admin |
| TC-02 | Pre-Screening — all pass | Pass | 2026-03-17 | admin |
| TC-03 | Edit Client Info | Pass | 2026-03-17 | admin |
| TC-04 | Fill Loan Info | Pass | 2026-03-17 | Fatima Abrahams |
| TC-05 | Initiate Loan Application | Pass | 2026-03-17 | Fatima Abrahams |
| TC-05a | Initiate without Amount (negative) | Pass | 2026-03-17 | Fatima Abrahams |
| TC-05b | Initiate without Product (negative) | Pass | 2026-03-17 | Fatima Abrahams |
| TC-06 | Confirm Verification Outcomes | Pass | 2026-03-17 | Fatima Abrahams |
| TC-07 | Complete Onboarding Checklist | Pass | 2026-03-17 | Fatima Abrahams |

**Lead:** IanH33468 Houvet (ID: ff08469e-0c25-4567-bcb5-d0c9b65e3a55)
**Opportunity:** IanH33468 Houvet (ID: 1f0baf9d-fb25-4cc7-970d-79d0bee540f5)
**Workflow Ref:** LA2026/0882

---

## Still To Test

1. **Negative pre-screening** — what happens when a disqualifying answer is given?
2. **Flag As High Risk** — alternative path at verification step
3. **Incomplete onboarding checklist** — can it be submitted with unchecked items?
4. **Entity loan application** — same flow but with Entity type (Directors, Signatories, Marital Regime)
5. **Farm addition** — add farm before initiating workflow
6. **Multiple products** — can more than one product be selected?
7. **Multiple loan purposes** — add several rows with different purposes
8. **Edit after workflow start** — can Client Info be edited while in Verification In Progress?
9. **Different RM role** — test with other RM accounts (Bonolo Lebelo, etc.)
10. **Compliance tab** — visible for admin but not RM; what does it contain?
