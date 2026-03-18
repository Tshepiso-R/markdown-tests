# Test Plan: Negative Paths & Edge Cases — LandBank CRM Loan Application

## Meta
| Field        | Value                                                              |
|-------------|--------------------------------------------------------------------|
| Module      | Negative & Edge Cases — Pre-Screening, Loan Validation, Workflow   |
| URL         | {{BASE_URL}} = landbankcrm-adminportal-qa.shesha.app               |
| Prereqs     | Admin account; RM account (Fatima); existing leads and opportunities for reuse |
| Last tested | —                                                                  |
| Status      | Not yet run                                                        |
| Test Data   | Reuse existing leads/opportunities where possible; create new only when required |

---

## User Journey Overview

```
This test plan covers negative paths and edge cases across the full loan application journey.
It is NOT a sequential flow — each test case is independent and targets a specific failure
or boundary condition.

AREA 1: Pre-Screening Failures (TC-NEG-01 to TC-NEG-03)
  └─ Disqualifying answers, missing checkbox

AREA 2: Loan Application Validation (TC-NEG-04 to TC-NEG-06)
  └─ Missing amount, missing product, missing owner

AREA 3: Field Validation (TC-NEG-07 to TC-NEG-10)
  └─ Invalid ID, duplicate ID, empty mandatory fields, invalid email

AREA 4: Workflow Edge Cases (TC-EDGE-01 to TC-EDGE-04)
  └─ High risk flag, edit after workflow start, partial checklist, navigation persistence

AREA 5: Entity-Specific Edge Cases (TC-EDGE-05 to TC-EDGE-08)
  └─ Zero directors, zero signatories, missing spouse details, director removal

AREA 6: Data Integrity (TC-EDGE-09 to TC-EDGE-10)
  └─ Province-region mapping, Google Places address formats
```

---

## Accounts Used

| Role | Username | Password | Used In |
|------|----------|----------|---------|
| System Administrator | admin | 123qwe | TC-NEG-01 to TC-NEG-03, TC-NEG-07 to TC-NEG-10, TC-EDGE-05 to TC-EDGE-10 |
| RM (Relationship Manager) | fatima.abrahams@landbank.co.za | 123qwe | TC-NEG-04 to TC-NEG-06, TC-EDGE-01 to TC-EDGE-04 |

---

## AREA 1: Pre-Screening Failures

### TC-NEG-01: Pre-screening with disqualifying answer — "Is the client blacklisted?" = Yes
- **Type:** Negative
- **Login:** admin
- **Prereqs:** Create a new Individual lead (or reuse an unconverted lead with status "New")
- **Steps:**
  1. Navigate to Leads table via sidebar menu
  2. Open a lead with status "New"
  3. Click "Initiate Pre-Screening"
  4. Answer questions as follows:
     | # | Question | Answer |
     |---|----------|--------|
     | 1 | Is the applicant a South African citizen? | Yes |
     | 2 | Is the farming land located in South Africa? | Yes |
     | 3 | Do the intended farming activities fall within the Land Bank mandate? | Yes |
     | 4 | Is the client blacklisted? | **Yes** (disqualifying) |
     | 5 | Is the client currently under debt review? | No |
     | 6 | Is the client's current Country of Residence South Africa? | Yes |
     | 7 | Does the client currently have access to suitable land for farming activities? | Yes |
  5. Tick the confirmation checkbox
  6. Click "Submit"
- **Expected result:** Pre-screening fails; "Pre-assessment failed!" message shown; no opportunity created
- **Assertions:**
  - [ ] "Pre-assessment failed!" message is displayed
  - [ ] Lead status does NOT change to "Converted" (remains "New" or changes to a failed state)
  - [ ] Assessment field shows "Failed" (if applicable)
  - [ ] No "Converted To Opportunity" link appears
  - [ ] No "Converted To Account" link appears
  - [ ] "Initiate Pre-Screening" button behavior after failure (does it reappear or remain hidden?)

### TC-NEG-02: Pre-screening with "No" on SA citizen question
- **Type:** Negative
- **Login:** admin
- **Prereqs:** Create a new Individual lead (or reuse an unconverted lead with status "New")
- **Steps:**
  1. Navigate to Leads table via sidebar menu
  2. Open a lead with status "New"
  3. Click "Initiate Pre-Screening"
  4. Answer questions as follows:
     | # | Question | Answer |
     |---|----------|--------|
     | 1 | Is the applicant a South African citizen? | **No** (disqualifying) |
     | 2 | Is the farming land located in South Africa? | Yes |
     | 3 | Do the intended farming activities fall within the Land Bank mandate? | Yes |
     | 4 | Is the client blacklisted? | No |
     | 5 | Is the client currently under debt review? | No |
     | 6 | Is the client's current Country of Residence South Africa? | Yes |
     | 7 | Does the client currently have access to suitable land for farming activities? | Yes |
  5. Tick the confirmation checkbox
  6. Click "Submit"
- **Expected result:** Pre-screening fails; "Pre-assessment failed!" message shown; no opportunity created
- **Assertions:**
  - [ ] "Pre-assessment failed!" message is displayed
  - [ ] Lead status does NOT change to "Converted"
  - [ ] No "Converted To Opportunity" link appears
  - [ ] No "Converted To Account" link appears

### TC-NEG-03: Submit pre-screening without ticking confirmation checkbox
- **Type:** Negative
- **Login:** admin
- **Prereqs:** Create a new Individual lead (or reuse an unconverted lead with status "New")
- **Steps:**
  1. Navigate to Leads table via sidebar menu
  2. Open a lead with status "New"
  3. Click "Initiate Pre-Screening"
  4. Answer all 7 questions with qualifying answers (all pass)
  5. Do NOT tick the confirmation checkbox
  6. Observe the "Submit" button state
- **Expected result:** "Submit" button remains disabled; cannot submit without confirmation
- **Assertions:**
  - [ ] "Submit" button is disabled (greyed out or non-clickable)
  - [ ] No submission occurs
  - [ ] No status change on the lead

---

## AREA 2: Loan Application Validation

### TC-NEG-04: Initiate Loan Application without Requested Amount (Amount = 0)
- **Type:** Negative
- **Login:** RM (fatima.abrahams@landbank.co.za)
- **Prereqs:** Opportunity in Draft status with Product selected but Requested Amount = 0 or empty
- **Steps:**
  1. Navigate to Opportunities table via sidebar menu
  2. Open an opportunity in Draft status
  3. Ensure a Product is selected (Loan Info tab)
  4. Ensure Requested Amount is 0 or empty
  5. Click "Initiate Loan Application"
- **Expected result:** Error message blocks workflow initiation
- **Assertions:**
  - [ ] Error message: "Cannot initiate workflow: requested amount must be greater than zero."
  - [ ] Opportunity status remains "Draft"
  - [ ] No workflow item created in Inbox

### TC-NEG-05: Initiate Loan Application without Product selected
- **Type:** Negative
- **Login:** RM (fatima.abrahams@landbank.co.za)
- **Prereqs:** Opportunity in Draft status with Requested Amount > 0 but no Product selected
- **Steps:**
  1. Navigate to Opportunities table via sidebar menu
  2. Open an opportunity in Draft status
  3. Ensure no Product is selected (Loan Info tab — Products field empty)
  4. Ensure Requested Amount > 0
  5. Click "Initiate Loan Application"
- **Expected result:** Error message blocks workflow initiation
- **Assertions:**
  - [ ] Error message: "Cannot initiate workflow: at least one product is required."
  - [ ] Opportunity status remains "Draft"
  - [ ] No workflow item created in Inbox

### TC-NEG-06: Initiate Loan Application without Opportunity Owner set
- **Type:** Negative
- **Login:** RM (fatima.abrahams@landbank.co.za)
- **Prereqs:** Opportunity in Draft status with Product selected, Amount > 0, but Opportunity Owner cleared/empty
- **Steps:**
  1. Navigate to Opportunities table via sidebar menu
  2. Open an opportunity in Draft status
  3. Click "Edit"
  4. Clear the Opportunity Owner field (if possible)
  5. Click "Save"
  6. Click "Initiate Loan Application"
- **Expected result:** Error message blocks workflow initiation or Save fails without Owner
- **Assertions:**
  - [ ] Error message displayed (document exact wording)
  - [ ] Opportunity status remains "Draft"
  - [ ] No workflow item created in Inbox
  - [ ] Document whether Owner field can be cleared at all

---

## AREA 3: Field Validation

### TC-NEG-07: Enter invalid ID number (less than 13 digits)
- **Type:** Negative
- **Login:** admin
- **Prereqs:** Opportunity in Draft status (Personal type)
- **Steps:**
  1. Navigate to an opportunity in Draft status via sidebar menu
  2. Click "Edit"
  3. In Client ID Number field, enter "12345" (only 5 digits)
  4. Click "Save"
- **Expected result:** Validation error — ID number must be 13 digits
- **Assertions:**
  - [ ] Validation error message displayed for ID Number field
  - [ ] Document exact error message text
  - [ ] Data is NOT saved with invalid ID
  - [ ] Test with other invalid lengths: 12 digits, 14 digits, alphabetic characters

### TC-NEG-08: Enter duplicate ID number for two directors (Entity)
- **Type:** Negative
- **Login:** admin
- **Prereqs:** Entity opportunity in Draft status
- **Steps:**
  1. Navigate to an Entity opportunity in Draft status via sidebar menu
  2. Click "Edit"
  3. Add Director 1 with ID Number: 7708206169188
  4. Add Director 2 with the same ID Number: 7708206169188
  5. Click "Save"
- **Expected result:** Document behavior — does the system show an error for duplicate IDs or allow it?
- **Assertions:**
  - [ ] Document whether duplicate ID is accepted or rejected
  - [ ] If rejected: note the exact error message
  - [ ] If accepted: note this as a potential data integrity issue
  - [ ] Both directors appear in the Directors list (or only one)

### TC-NEG-09: Leave mandatory fields empty and try to Save
- **Type:** Negative
- **Login:** admin
- **Prereqs:** Opportunity in Draft status (Personal type)
- **Steps:**
  1. Navigate to an opportunity in Draft status via sidebar menu
  2. Click "Edit"
  3. Clear the following mandatory fields (if they have values):
     - Client Name
     - Client Surname
     - Email Address
     - Mobile Number
  4. Click "Save"
- **Expected result:** Validation errors shown for all mandatory fields
- **Assertions:**
  - [ ] Validation error for Client Name (document exact message)
  - [ ] Validation error for Client Surname (document exact message)
  - [ ] Validation error for Email Address (document exact message)
  - [ ] Validation error for Mobile Number (document exact message)
  - [ ] Data is NOT saved with empty mandatory fields
  - [ ] Document which fields are truly mandatory vs optional

### TC-NEG-10: Enter invalid email format
- **Type:** Negative
- **Login:** admin
- **Prereqs:** Opportunity in Draft status (Personal type)
- **Steps:**
  1. Navigate to an opportunity in Draft status via sidebar menu
  2. Click "Edit"
  3. In Email Address field, enter "not-an-email" (no @ symbol)
  4. Click "Save"
- **Input data:**
  | Test Value | Expected Outcome |
  |-----------|-----------------|
  | not-an-email | Validation error |
  | user@ | Validation error |
  | @domain.com | Validation error |
  | user@domain | Document behavior (technically valid but unusual) |
- **Expected result:** Validation error for invalid email format
- **Assertions:**
  - [ ] Validation error message displayed for email field
  - [ ] Document exact error message text
  - [ ] Data is NOT saved with invalid email
  - [ ] Test multiple invalid formats and document results

---

## AREA 4: Workflow Edge Cases

### TC-EDGE-01: Flag As High Risk at verification step instead of Finalise
- **Type:** Edge case
- **Login:** RM (fatima.abrahams@landbank.co.za)
- **Prereqs:** Opportunity with workflow at "Confirm verification outcomes" step (Verification In Progress)
- **Steps:**
  1. Navigate to Inbox via sidebar menu
  2. Open a workflow item at "Confirm verification outcomes" step
  3. Review verification details
  4. Instead of clicking "Finalise Verification Outcomes", click "Flag As High Risk"
  5. Observe what happens — document the workflow path
- **Expected result:** Document the alternative workflow path
- **Assertions:**
  - [ ] Document what dialog/confirmation appears after clicking "Flag As High Risk"
  - [ ] Document the new workflow status after flagging
  - [ ] Document the new opportunity status
  - [ ] Document what action is required next (if any)
  - [ ] Document whether the workflow can be resumed or is terminated
  - [ ] Document whether the opportunity can be reverted to normal flow

### TC-EDGE-02: Edit Client Info after workflow is in "Verification In Progress"
- **Type:** Edge case
- **Login:** RM (fatima.abrahams@landbank.co.za)
- **Prereqs:** Opportunity with status "Verification In Progress" (workflow already initiated)
- **Steps:**
  1. Navigate to Opportunities table via sidebar menu
  2. Open the opportunity that is in "Verification In Progress" status
  3. Attempt to click "Edit"
  4. If edit mode is available, try to change Client Name or other fields
  5. If edit mode is available, try to click "Save"
- **Expected result:** Document whether fields can still be edited after workflow initiation
- **Assertions:**
  - [ ] Document whether "Edit" button is visible
  - [ ] Document whether "Edit" button is clickable
  - [ ] Document which fields (if any) are editable vs read-only
  - [ ] Document whether changes can be saved
  - [ ] Document whether changes affect the running workflow

### TC-EDGE-03: Submit onboarding checklist with unchecked items
- **Type:** Edge case
- **Login:** RM (fatima.abrahams@landbank.co.za)
- **Prereqs:** Workflow at "Complete Onboarding Checklist" step
- **Steps:**
  1. Navigate to the "Complete Onboarding Checklist" workflow step (via Inbox)
  2. Select Years Of Farming Experience (mandatory dropdown)
  3. Leave ALL checklist items unchecked
  4. Click "Submit"
  5. If submission is blocked, check one item and retry
- **Expected result:** Document whether partial/empty checklist submission is allowed
- **Assertions:**
  - [ ] Document whether "Submit" is enabled with no items checked
  - [ ] Document whether submission succeeds with no items checked
  - [ ] Document whether any specific items are mandatory
  - [ ] If blocked: document exact error message
  - [ ] If allowed: document whether workflow still completes

### TC-EDGE-04: Navigate away from workflow page and return
- **Type:** Edge case
- **Login:** RM (fatima.abrahams@landbank.co.za)
- **Prereqs:** Workflow at any active step (e.g., "Confirm verification outcomes" or "Complete Onboarding Checklist")
- **Steps:**
  1. Open a workflow item from Inbox
  2. Note the current step and any data entered
  3. Navigate to a different page (e.g., Opportunities table) via sidebar menu
  4. Navigate back to Inbox via sidebar menu
  5. Re-open the same workflow item
- **Expected result:** Document whether workflow state persists
- **Assertions:**
  - [ ] Workflow item still appears in Inbox
  - [ ] Workflow is at the same step as before navigation
  - [ ] Any previously entered data (e.g., checklist selections) persists or is lost
  - [ ] No duplicate workflow items created

---

## AREA 5: Entity-Specific Edge Cases

### TC-EDGE-05: Create entity opportunity with 0 directors — can workflow be initiated?
- **Type:** Edge case
- **Login:** admin
- **Prereqs:** Entity opportunity in Draft status with all other fields filled (Entity Info, Loan Info, Product, Amount > 0) but NO directors added
- **Steps:**
  1. Navigate to an Entity opportunity in Draft status via sidebar menu
  2. Verify Directors section is empty (0 directors)
  3. Ensure Product is selected and Amount > 0
  4. Click "Initiate Loan Application"
- **Expected result:** Document whether workflow initiation is blocked or allowed without directors
- **Assertions:**
  - [ ] Document whether "Initiate Loan Application" button is enabled
  - [ ] Document whether an error message appears
  - [ ] If error: document exact error message
  - [ ] If allowed: document what happens at verification step without directors

### TC-EDGE-06: Create entity opportunity with 0 signatories — can workflow be initiated?
- **Type:** Edge case
- **Login:** admin
- **Prereqs:** Entity opportunity in Draft status with directors added but NO signatories
- **Steps:**
  1. Navigate to an Entity opportunity in Draft status via sidebar menu
  2. Verify Signatories section is empty (0 signatories)
  3. Ensure Directors are added, Product is selected, and Amount > 0
  4. Click "Initiate Loan Application"
- **Expected result:** Document whether workflow initiation is blocked or allowed without signatories
- **Assertions:**
  - [ ] Document whether "Initiate Loan Application" button is enabled
  - [ ] Document whether an error message appears
  - [ ] If error: document exact error message
  - [ ] If allowed: document what happens at verification step without signatories

### TC-EDGE-07: Add director with Married status but don't fill spouse details
- **Type:** Edge case
- **Login:** admin
- **Prereqs:** Entity opportunity in Draft status
- **Steps:**
  1. Navigate to an Entity opportunity in Draft status via sidebar menu
  2. Click "Edit"
  3. In Directors section, add a new director
  4. Fill required fields (First Name, Last Name, ID Number, Email, Mobile)
  5. Set Marital Status: Married
  6. Set Marital Regime: Married in Community of Property
  7. Leave Spouse First Name, Spouse Last Name, and Spouse ID Number empty
  8. Click "Save"
- **Expected result:** Document whether save is blocked or allowed without spouse details
- **Assertions:**
  - [ ] Document whether validation error appears for empty spouse fields
  - [ ] If error: document exact error messages
  - [ ] If allowed: document whether spouse fields are truly optional
  - [ ] Document behavior at verification step if spouse details are missing

### TC-EDGE-08: Remove a director after adding — verify table updates
- **Type:** Edge case
- **Login:** admin
- **Prereqs:** Entity opportunity with at least 2 directors already added
- **Steps:**
  1. Navigate to an Entity opportunity with directors via sidebar menu
  2. Click "Edit"
  3. Note the current number of directors in the Directors table
  4. Click the remove/delete button on one director row (if available)
  5. Click "Save"
  6. Verify the Directors table count
- **Expected result:** Director is removed and table updates correctly
- **Assertions:**
  - [ ] Document whether a delete/remove button exists on director rows
  - [ ] Document whether a confirmation dialog appears before removal
  - [ ] Director count decreases by 1 after removal
  - [ ] Removed director no longer appears in the Directors table
  - [ ] "Data saved successfully!" confirmation after save
  - [ ] If removal is not possible: document this limitation

---

## AREA 6: Data Integrity

### TC-EDGE-09: Verify Province to Region auto-mapping for all 9 provinces
- **Type:** Edge case
- **Login:** admin
- **Prereqs:** Opportunity in Draft status (Personal type)
- **Steps:**
  1. Navigate to an opportunity in Draft status via sidebar menu
  2. Click "Edit"
  3. For each province, set the Province field and observe the Region field auto-mapping
  4. Record the mapping for all 9 provinces
- **Expected mapping (verify):**
  | Province | Expected Region |
  |----------|----------------|
  | Eastern Cape | Eastern Region |
  | Free State | Central Region |
  | Gauteng | Central Region |
  | KwaZulu-Natal | Eastern Region |
  | Limpopo | Northern Region |
  | Mpumalanga | Northern Region |
  | North West | Central Region |
  | Northern Cape | Western Region |
  | Western Cape | Western Region |
- **Expected result:** All 9 provinces map to the correct region automatically
- **Assertions:**
  - [ ] Eastern Cape → (document actual region)
  - [ ] Free State → (document actual region)
  - [ ] Gauteng → Central Region (confirmed in previous tests)
  - [ ] KwaZulu-Natal → (document actual region)
  - [ ] Limpopo → (document actual region)
  - [ ] Mpumalanga → (document actual region)
  - [ ] North West → (document actual region)
  - [ ] Northern Cape → (document actual region)
  - [ ] Western Cape → (document actual region)

### TC-EDGE-10: Verify Google Places address auto-fill works for different address formats
- **Type:** Edge case
- **Login:** admin
- **Prereqs:** Opportunity in Draft status
- **Steps:**
  1. Navigate to an opportunity in Draft status via sidebar menu
  2. Click "Edit"
  3. Click on the Residential/Registered Address field
  4. Test the following address searches:
     | Search Input | Expected Behavior |
     |-------------|-------------------|
     | 100 Main Street, Johannesburg | Google Places dropdown with suggestions |
     | Hatfield, Pretoria | Google Places dropdown with suggestions |
     | 1 Jan Smuts Avenue, Rosebank | Google Places dropdown with suggestions |
     | Rural address (farm name) | Document whether farm addresses resolve |
  5. Select an address from the dropdown
  6. Verify the address fields are auto-filled
- **Expected result:** Google Places provides suggestions and auto-fills address fields
- **Assertions:**
  - [ ] Google Places dropdown appears when typing an address
  - [ ] Selecting an address auto-fills the address field
  - [ ] Province field updates based on selected address (if applicable)
  - [ ] Region field auto-maps based on province
  - [ ] Document whether rural/farm addresses resolve correctly
  - [ ] Document any address formats that fail to resolve

---

## Rules

- Each test case is independent — no sequential dependency between test cases
- Reuse existing leads and opportunities where possible to avoid creating unnecessary test data
- For test cases that require a specific state (e.g., workflow in progress), set up the state first or reuse an opportunity from a previous test run
- If a test case requires a fresh lead, create one with a unique first name (e.g., NEG01-XXXXX)
- Always snapshot the browser before interacting with any element
- On failure: take a screenshot, document the actual behavior, and continue to the next test case
- For "document behavior" test cases, record every observation — these are exploratory
- Do not assume the expected behavior for edge cases — observe and document what actually happens

---

## Test Execution Record

| TC | Description | Result | Date | Tester |
|----|-------------|--------|------|--------|
| TC-NEG-01 | Pre-screening: blacklisted = Yes | — | — | — |
| TC-NEG-02 | Pre-screening: SA citizen = No | — | — | — |
| TC-NEG-03 | Pre-screening: no confirmation checkbox | — | — | — |
| TC-NEG-04 | Initiate without Requested Amount | — | — | — |
| TC-NEG-05 | Initiate without Product | — | — | — |
| TC-NEG-06 | Initiate without Opportunity Owner | — | — | — |
| TC-NEG-07 | Invalid ID number (< 13 digits) | — | — | — |
| TC-NEG-08 | Duplicate ID for two directors | — | — | — |
| TC-NEG-09 | Empty mandatory fields | — | — | — |
| TC-NEG-10 | Invalid email format | — | — | — |
| TC-EDGE-01 | Flag As High Risk at verification | — | — | — |
| TC-EDGE-02 | Edit after workflow started | — | — | — |
| TC-EDGE-03 | Submit checklist with unchecked items | — | — | — |
| TC-EDGE-04 | Navigate away and return to workflow | — | — | — |
| TC-EDGE-05 | Entity with 0 directors | — | — | — |
| TC-EDGE-06 | Entity with 0 signatories | — | — | — |
| TC-EDGE-07 | Married director without spouse details | — | — | — |
| TC-EDGE-08 | Remove director after adding | — | — | — |
| TC-EDGE-09 | Province → Region mapping (all 9) | — | — | — |
| TC-EDGE-10 | Google Places address formats | — | — | — |
