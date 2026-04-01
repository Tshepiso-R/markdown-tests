# Test Plan: [Module Name]

## How To Run This Test Plan

> **This is NOT a Playwright test.** Do not generate Playwright scripts, test files, or any automated test code.

**Before executing:**
1. Read `CLAUDE.md` (project root) — understand how this project works
2. Read `test-plans/RULES.md` — execution rules that govern every test run
3. Read this test plan fully before touching the browser

**Execution method:** Claude drives the browser directly using MCP browser tools (`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_fill_form`, etc.). Each step is executed manually through the browser — snapshot before acting, click/fill using element refs from the snapshot, snapshot after to verify.

**Do NOT:**
- Generate Playwright, Cypress, Selenium, or any other test framework code
- Write `.spec.ts`, `.test.js`, or any script files
- Use `browser_evaluate` for UI interaction — only `browser_snapshot` + MCP actions
- Skip reading RULES.md or CLAUDE.md before starting

---

## Meta
| Field        | Value                                                              |
|-------------|--------------------------------------------------------------------|
| Module      | e.g. Full Journey — Lead → Opportunity → Workflow → Complete       |
| URL         | {{BASE_URL}} = landbankcrm-adminportal-qa.shesha.app               |
| Prereqs     | e.g. Admin account for lead creation; RM account (Fatima) for workflow |
| Last tested | YYYY-MM-DD                                                         |
| Status      | Pass / Fail / Partial / Not yet run                                |
| Test Data   | e.g. Ian Houvet, ID: 7708206169188, Email: 5s9ku.consent-[timestamp]@inbox.testmail.app |

---

## Reports

| Date | Report | Trigger | Result |
|------|--------|---------|--------|
| YYYY-MM-DD | [Report Name](../test-reports/[module]/[report-file].md) | Scheduled / Manual / CI | Pass / Fail |

---

## User Journey Overview

```
Describe the full user journey as a tree:

PHASE 1: [First step]
  └─ [Action]
       └─ [Expected status change]

PHASE 2: [Next step]
  └─ [Action]
       └─ [Expected status change]
```

---

## Accounts Used

| Role | Username | Password | Used In |
|------|----------|----------|---------|
| System Administrator | admin | (from env) | Phase 1, Phase 2 |
| RM (Relationship Manager) | fatima.abrahams@landbank.co.za | (from env) | Phase 3–6 |

---

## PHASE 1: [Phase Name]

### TC-01: [Short description]
- **Type:** Happy path
- **Login:** admin
- **URL:** {{BASE_URL}}/dynamic/[module]/[page]
- **Steps:**
  1. Navigate to [page] via sidebar menu
  2. Click [button]
  3. Fill all required fields (see input data)
  4. Click [submit button]
- **Input data:**
  | Field | Value | Type | Required |
  |-------|-------|------|----------|
  | Field Name | Value | Text / Dropdown / Searchable dropdown / Checkbox | Yes / No |
  | Field Name | Value | Type | Yes / No |
- **Expected result:** [What should happen — toast message, status change, etc.]
- **Assertions:**
  - [ ] [Specific thing to verify — e.g. toast message text]
  - [ ] [Status badge shows expected value]
  - [ ] [Record visible in table]
  - [ ] [All fields saved correctly]

### Dropdown Values — [Section Name]
| Field | Options |
|-------|---------|
| Field Name | Option1, Option2, Option3 |

---

## PHASE 2: [Phase Name]

### TC-02: [Short description]
- **Type:** Happy path
- **Login:** admin or RM
- **Steps:**
  1. [Action]
  2. [Action]
- **Expected result:** [What should happen]
- **Assertions:**
  - [ ] [Assertion 1]
  - [ ] [Assertion 2]

### TC-03: [Short description — negative test]
- **Type:** Negative
- **Steps:**
  1. [Action that should fail]
- **Expected result:** Error message shown
- **Assertions:**
  - [ ] Error: "[expected error message]"
  - [ ] Status remains unchanged

---

## Status Lifecycle Summary

| Phase | Action | Status | Workflow Status |
|-------|--------|--------|-----------------|
| Phase 1 | [Action] | [Status] | — |
| Phase 2 | [Action] | [Status] | — |
| Phase 3 | [Action] | [Status] | In Progress |

---

## Rules

> Module-specific rules that override or extend RULES.md.

- [Rule 1 — e.g. specific field must be filled before workflow can start]
- [Rule 2 — e.g. province auto-maps to region]
- [Rule 3 — e.g. conditional fields appear when X is selected]

---

## Test Execution Record

| TC | Description | Result | Date | Tester |
|----|-------------|--------|------|--------|
| TC-01 | [Description] | Pass / Fail | YYYY-MM-DD | [Who ran it] |
| TC-02 | [Description] | Pass / Fail | YYYY-MM-DD | [Who ran it] |

**Lead:** [Name] (ID: [guid])
**Opportunity:** [Name] (ID: [guid])
**Workflow Ref:** [Ref number]

---

## Still To Test

1. [Scenario not yet covered]
2. [Edge case to investigate]
3. [Alternative path to test]
