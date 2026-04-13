# Test Plan: [Module Name]

> **Not a Playwright test.** Claude drives the browser directly via MCP tools.
> Before executing: read `CLAUDE.md` → `test-plans/RULES.md` → this plan (in full).

---

## Meta

| Field        | Value                                                              |
|-------------|--------------------------------------------------------------------|
| Module      | e.g. Full Journey — Lead → Opportunity → Workflow → Complete       |
| App         | e.g. LandBank CRM (QA) / SA Gov Bursary Management (DEV)          |
| URL         | {{BASE_URL}} = landbankcrm-adminportal-qa.shesha.app               |
| Prereqs     | e.g. Admin account for lead creation; RM account (Fatima) for workflow |
| Last tested | YYYY-MM-DD                                                         |
| Status      | Pass / Fail / Partial / Not yet run                                |
| Test Data   | e.g. Ian Houvet, ID: 7708206169188, Email: guwn6.consent-[timestamp]@inbox.testmail.app |

---

## Reports

| Date | Report | Trigger | Result |
|------|--------|---------|--------|
| YYYY-MM-DD | [Report Name](../test-reports/[module]/[report-file].md) | Manual / CI | Pass / Fail |

---

## Azure DevOps

| Field | Value |
|-------|-------|
| AzDO Plan ID | _(populated after sync)_ |
| AzDO Plan URL | _(populated after sync)_ |
| Last synced | _(populated after sync)_ |

> Sync: "Sync this test plan to Azure DevOps" — see `azdo-sync/SYNC-PLAYBOOK.md`

---

## User Journey Overview

```
PHASE 1: [First step]
  └─ [Action]
       └─ [Expected status change]

PHASE 2: [Next step]
  └─ [Action]
       └─ [Expected status change]

For non-sequential plans (negative/edge cases), use AREA instead of PHASE:

AREA 1: [Category]
  └─ [What is being tested]
```

---

## Accounts Used

| Role | Username | Password | Used In |
|------|----------|----------|---------|
| System Administrator | admin | (from env) | Phase 1, Phase 2 |
| RM (Relationship Manager) | fatima.abrahams@landbank.co.za | (from env) | Phase 3–6 |

> Never hardcode passwords in plans — use env variables or `(from env)` placeholder.

---

## PHASE 1: [Phase Name]

### TC-01: [Short description]
- **Type:** Happy path / Negative / Edge case
- **Login:** admin
- **Prereqs:** None (first test) / TC-XX must pass / [specific state required]
- **Steps:**
  1. Navigate to [page] via sidebar menu
  2. Click [button]
  3. Fill all required fields (see input data)
  4. Click [submit button]
- **Input data:**
  | Field | Value | Type | Required |
  |-------|-------|------|----------|
  | Field Name | Value | Text / Dropdown / Searchable dropdown / Checkbox | Yes / No |
- **Expected result:** [What should happen — toast message, status change, redirect, etc.]
- **Assertions:**
  - [ ] [Toast message text — e.g. "Data saved successfully!"]
  - [ ] [Status badge shows expected value]
  - [ ] [Record visible in table / link appears / button disappears]
  - [ ] [All fields saved correctly — check ALL tabs after save]

### Dropdown Values — [Section Name]
| Field | Options |
|-------|---------|
| Field Name | Option1, Option2, Option3 |

---

## PHASE 2: [Phase Name]

### TC-02: [Short description]
- **Type:** Happy path
- **Login:** admin or RM
- **Prereqs:** TC-01 must pass
- **Steps:**
  1. [Action — be specific: "Click Edit", "Switch to Loan Info tab"]
  2. [Action]
- **Expected result:** [What should happen]
- **Assertions:**
  - [ ] [Assertion 1]
  - [ ] [Assertion 2]

### TC-03: [Short description — negative test]
- **Type:** Negative
- **Login:** admin
- **Prereqs:** [State needed — e.g. "An unconverted lead with status New"]
- **Steps:**
  1. [Action that should fail — be specific about what to do wrong]
- **Expected result:** Error message shown, no state change
- **Assertions:**
  - [ ] Error: "[expected error message text]"
  - [ ] Status remains [expected status]

---

## Consent / OTP Flow (if applicable)

> Delete this section if the module doesn't involve consent.

| Step | Action | Expected |
|------|--------|----------|
| 1 | [Trigger action] | Status → [e.g. Consent Pending] |
| 2 | Retrieve email via testmail.app API (tag: `consent-[timestamp]`) | Subject: "[expected subject]" |
| 3 | Extract URL from email, open in browser | [Expected page loads] |
| 4 | Request OTP → retrieve OTP email → submit | OTP accepted |
| 5 | Sign consent/resolution | Status → [e.g. Verification In Progress] |

---

## Status Lifecycle Summary

| Phase | Action | Status | Workflow Status |
|-------|--------|--------|-----------------|
| Phase 1 | [Action] | [Status] | — |
| Phase 2 | [Action] | [Status] | — |
| Phase 3 | [Action] | [Status] | In Progress |

> Every status transition must be explicitly asserted in the test case.

---

## Module-Specific Rules

> Rules that override or extend `RULES.md` for this module.

- [Rule 1 — e.g. specific field must be filled before workflow can start]
- [Rule 2 — e.g. province auto-maps to region]
- [Rule 3 — e.g. conditional fields appear when X is selected]
- [Rule 4 — e.g. all directors must sign before status progresses]
