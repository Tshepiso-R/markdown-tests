# Loan Application Workflow — End-to-End Test Report

**Date:** 2026-03-17
**Tester:** Fatima Abrahams (fatima.abrahams@landbank.co.za / 123qwe)
**Environment:** QA (landbankcrm-adminportal-qa.shesha.app)
**Opportunity:** IanH33468 Houvet (ID: 1f0baf9d-fb25-4cc7-970d-79d0bee540f5)
**Workflow Ref:** LA2026/0882
**Client:** Ian Houvet (ID: 7708206169188, Email: promise.raganya@boxfusion.io)

---

## Run Summary
| Field          | Value       |
|---------------|-------------|
| Date          | 2026-03-17  |
| Total cases   | 5           |
| Passed        | 5           |
| Failed        | 0           |
| Skipped       | 0           |
| Duration      | ~20m        |

---

## Complete Workflow Lifecycle Discovered

```
Lead (New)
  → Pre-Screening (Pass)
    → Opportunity (Draft)
      → Fill Client Info, Loan Info (Products + Amount required)
        → Initiate Loan Application
          → Opportunity (Verification In Progress)
            → Workflow Step 1: Confirm Verification Outcomes
              - View verification details (ID Status, Photo Verification, KYC, Compliance)
              - Click "Finalise Verification Outcomes"
                → Workflow Step 2: Complete Onboarding Checklist
                  - Fill Pre-Onboarding Questions (9 items + 1 conditional)
                  - Click "Submit"
                    → Workflow: COMPLETED
                      → Opportunity (Complete)
```

### Status Lifecycle
| Stage | Opportunity Status | Workflow Status |
|-------|-------------------|-----------------|
| After lead conversion | Draft | — |
| After Initiate Loan Application | Verification In Progress | In Progress |
| After Finalise Verification | Verification In Progress | In Progress (next step) |
| After Submit Onboarding Checklist | Complete | Completed |

---

## Results

### Step 1: Fill Loan Info (prerequisite for workflow)
- **Result:** Pass
- **Notes:** "Initiate Loan Application" requires: Requested Amount > 0 AND at least one Product selected
- **Validation errors encountered:**
  1. "Cannot initiate workflow: requested amount must be greater than zero."
  2. "Cannot initiate workflow: at least one product is required."
- **Data filled:**
  | Field | Value |
  |-------|-------|
  | Products | R MT Loans (CB&T) — selected via entity picker |
  | Business Summary | Farming operations in Gauteng region |
  | Requested Amount | 500000 |
  | Existing Relationship with Bank | None |
  | Sources Of Income | Farming income |
  | Loan Purpose | Purchase Of Livestock — 500000 |

### Step 2: Initiate Loan Application
- **Result:** Pass
- **Message:** "Loan Application submitted successfully"
- **Status change:** Draft → Verification In Progress
- **Workflow created:** LA2026/0882

### Step 3: Confirm Verification Outcomes
- **Result:** Pass
- **Action Required:** "Confirm verification outcomes"
- **Verification Details (via "Awaiting Review" button):**
  | Verification | Status |
  |-------------|--------|
  | ID Status | Completed |
  | Photo Verification Status | Awaiting Review |
  | KYC Status | Initiated |
  | Compliance Verification | Completed |
- **Actions available:** "Finalise Verification Outcomes", "Flag As High Risk"
- **Action taken:** Clicked "Finalise Verification Outcomes"
- **Result:** Automatically moved to next workflow step

### Step 4: Complete Onboarding Checklist
- **Result:** Pass
- **Pre-Onboarding Questions:**
  | Question | Value |
  |----------|-------|
  | Years Of Farming Experience | 4 to 6 Years |
  | Does this operation require Water Use Rights? | Yes (checked) |
  | Support with applying for water rights required? | Yes (conditional — appeared after Water Use Rights checked) |
  | Business Plan Development Support required? | Yes |
  | Is there access to working Equipment and Mechanization? | Yes |
  | Does the client have a Valid Tax Clearance certificate? | Yes |
  | Does the client have access to established markets? | Yes |
  | Formal Financial Records or Statements maintained? | Yes |
  | Does the client have an actively engaged Mentor? | Yes |
  | Is the client Compliant with all applicable Labor Laws? | Yes |
- **Message:** "Checklist saved successfully."

### Step 5: Workflow Completion
- **Result:** Pass
- **Final workflow status:** COMPLETED
- **Final opportunity status:** Complete
- **Message:** "Requested action is not available" (no more workflow steps)

---

## Workflow Prerequisites Discovered

To initiate the loan application workflow, the following are **required**:
1. Opportunity Owner must be set
2. Requested Amount must be > 0
3. At least one Product must be selected
4. Client Info fields should be filled (Client Name, Surname, Email, Mobile, Preferred Communication, Client Classification are mandatory)

---

## Products Available (Entity Picker)

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
| (+ 7 more on page 2) | |

---

## Pre-Onboarding Checklist — Dropdown Values

### Years Of Farming Experience
Up to 2 Years, 2 to 4 Years, 4 to 6 Years, 6 to 10 Years, More than 10 Years

---

## Fatima Abrahams Role Observations

| Feature | Available | Notes |
|---------|-----------|-------|
| Dashboard (Management) | Yes | Shows "My Dashboard" |
| Inbox | Yes | 232 workflow items |
| Leads | Yes | Can create and view leads |
| Opportunities | Yes | Can edit and initiate workflow |
| Cases | No | Not in Fatima's menu |
| Reports | No | Not in Fatima's menu |
| Service Management | No | Not in Fatima's menu |
| Administration | No | Not in Fatima's menu |
| Configurations | No | Not in Fatima's menu |
| Compliance tab | No | Not visible on opportunity for Fatima |

---

## Issues Found
| # | Step | Severity | Description |
|---|------|----------|-------------|
| 1 | Step 1 | Medium | **No clear indication of prerequisites** — user must discover through error messages that Products and Amount are required before initiating workflow |
| 2 | Step 3 | Low | **Photo Verification "Awaiting Review" but auto-finalised** — verification was finalised despite Photo Verification still in "Awaiting Review" status. May be by design. |
| 3 | Step 3 | Info | **KYC Status "Initiated" not "Completed"** — workflow proceeded despite KYC not being completed. May be by design for testing. |
| 4 | All | Low | **Console errors persist** — executeScriptSync TypeError throughout all workflow steps |

---

## Recommendations
1. **Add clear validation messages** on the opportunity page showing what's needed before "Initiate Loan Application" can proceed
2. **Test "Flag As High Risk" path** — what happens when verification is flagged instead of finalised?
3. **Test with incomplete onboarding checklist** — can the checklist be submitted with unchecked items?
4. **Test Fatima's role permissions** — verify she cannot access admin/config areas
5. **Document the full status lifecycle** in the test plan for regression testing
