# Drift Detection Playbook

> Claude reads this file after completing a test run to detect changes between what the test plan expected and what actually happened. This catches UI renames, removed fields, changed messages, and altered workflows so the test plan stays accurate.

---

## When to Run

- **After every test execution**, before finalizing the report
- **On demand:** "Run drift detection on report X against plan Y"

---

## Step 1: Build the Expected Model

Read the source test plan and extract, per test case:

| Field | Where to Find It |
|-------|------------------|
| Button/link names | Steps: `Click "[name]"`, `Click [name]` |
| Toast messages | Assertions: text in quotes after toast/message keywords |
| Status labels | Assertions: `Status: "[value]"`, `status → "[value]"` |
| Field names | Input data table: Field column |
| Field values | Input data table: Value column |
| Validation errors | Assertions: `Error: "[text]"` |
| Step count | Number of items in Steps list |
| Expected result text | `- **Expected result:**` line |

---

## Step 2: Build the Actual Model

Read the test report and extract, per test case:

| Field | Where to Find It |
|-------|------------------|
| Buttons clicked | Steps Followed: `Clicked "[name]"` |
| Toast messages seen | Assertions: `[x]` or `[!]` lines mentioning toast/message |
| Status observed | Assertions: actual status text |
| Fields found/missing | Steps Followed: fields filled or noted as missing |
| Validation errors seen | Assertions: actual error text |
| Steps executed | Number of steps in Steps Followed |
| Actual result | Result: PASS/FAIL + failure reason if any |

---

## Step 3: Compare — What Counts as Drift

For each test case, compare expected vs actual:

| Check | Expected (Plan) | Actual (Report) | Drift Type | Severity |
|-------|----------------|-----------------|------------|----------|
| Button text | Step says `Click "New Lead"` | Report says clicked "Create New Lead" | **UI Rename** | Low |
| Toast message | `"Loan Application submitted successfully"` | Report saw different text | **Message Change** | Medium |
| Status label | `Status → "Consent Pending"` | Report saw "Awaiting Consent" | **Status Change** | Medium |
| Field presence | Input data lists "Provincial Office" | Report says field not found | **Field Removed** | High |
| New field | Not in plan | Report mentions filling unexpected field | **New Element** | Medium |
| Validation text | `Error: "Cannot initiate..."` | Different error message | **Validation Change** | Medium |
| Step count | Plan has 4 steps | Report followed 6 steps | **Flow Change** | Medium |
| Missing element | Plan expects a button/link | Report says element not visible | **Element Removed** | High |

### What is NOT Drift (Ignore)

- Whitespace or formatting differences
- Timestamps, dates, unique identifiers (lead names like `AutoCI12345`)
- Minor capitalization differences in non-UI text
- Report phrasing differences (e.g., "Clicked OK" vs step says "Click OK" — past tense is expected)
- Screenshots present/absent
- Test data values that are intentionally unique per run

---

## Step 4: Write the Changes Detected Section

If any drift is found, append this section to the test report **before** the final summary:

```markdown
---

## Changes Detected (Drift Report)

> Compared against: `test-plans/[plan-file].md`
> Detection date: YYYY-MM-DD

| # | TC | Type | Expected (Plan) | Actual (Run) | Severity |
|---|-----|------|-----------------|--------------|----------|
| 1 | TC-01 | UI Rename | Button: "New Lead" | Button: "Create New Lead" | Low |
| 2 | TC-05 | Message Change | Toast: "Loan Application submitted successfully" | Toast: "Application initiated" | Medium |
| 3 | TC-03 | Field Removed | Field: "Provincial Office" (dropdown) | Field not visible on page | High |

### Suggested Updates to Test Plan

> Review each suggestion. If the change is intentional (app was updated), apply the update.
> If the change is unexpected, file a bug instead.

1. **TC-01, Step 2:** Change `Click "New Lead"` to `Click "Create New Lead"`
   - File: `test-plans/[plan].md`, line ~XX
   - Also update Dropdown Values table if button is in a dropdown

2. **TC-05, Assertions:** Change toast text
   - Old: `"Loan Application submitted successfully"`
   - New: `"Application initiated"`

3. **TC-03, Input data:** Remove or mark "Provincial Office" as conditional
   - The field may have been removed or hidden behind a condition
   - Verify with the dev team before removing from plan

### Impact on Azure DevOps Test Cases

If these updates are applied to the test plan, re-sync to Azure DevOps:
- Run: "Re-sync [plan] to Azure DevOps"
- This will update the affected test case steps in AzDO
```

---

## Step 5: Summary Output

After writing the drift section, print:

```
Drift detection complete:
  - Test cases compared: N
  - Changes detected: N (X high, Y medium, Z low)
  - See "Changes Detected" section in the report
  - Action required: Review suggested updates and decide whether to apply
```

If **no drift** was detected:

```
Drift detection complete:
  - Test cases compared: N
  - No changes detected — test plan is up to date
```

---

## Severity Guide

| Severity | Meaning | Action |
|----------|---------|--------|
| **High** | Element removed, flow broken, test case can't complete as written | Must update test plan or file a bug |
| **Medium** | Text changed, status renamed, new validation — test case still works but assertions are wrong | Should update test plan |
| **Low** | Minor rename, cosmetic change — test case passes but wording is outdated | Nice to update, not blocking |

---

## Rules

- **Never auto-apply** changes to the test plan — always present as suggestions
- **Never mark drift as a test failure** — drift means the app changed, not that it's broken
- A test case can **PASS** (functionally worked) but still have **drift** (wording doesn't match plan)
- If a test case **FAILed** due to drift (e.g., button removed so step couldn't execute), note both the failure AND the drift
- Keep drift detection **separate** from pass/fail assessment — they answer different questions
