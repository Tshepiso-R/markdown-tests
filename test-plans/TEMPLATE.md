# Test Plan: [Module Name]

## Meta
| Field        | Value                     |
|-------------|---------------------------|
| Module      | e.g. Lead Creation        |
| URL         | e.g. /leads/create        |
| Prereqs     | e.g. Logged in as agent   |
| Last tested | YYYY-MM-DD                |
| Status      | Pass / Fail / Partial     |

---

## Flow

> Describe the user journey step by step. Claude will follow these steps using the browser.

1. Navigate to [page]
2. Fill in [field] with [value]
3. Click [button]
4. Expect [outcome]

---

## Test Cases

### TC-01: [Short description]
- **Type:** Happy path | Negative | Edge case
- **Steps:**
  1. [Action]
  2. [Action]
- **Input data:**
  | Field       | Value              |
  |------------|--------------------|
  | First Name | Test               |
  | Last Name  | User               |
- **Expected result:** [What should happen]
- **Assertions:**
  - [ ] [Specific thing to verify]
  - [ ] [Another thing to verify]

### TC-02: [Short description]
- **Type:** Negative
- **Steps:**
  1. [Action]
  2. Leave [field] empty
  3. Click submit
- **Expected result:** Validation error shown
- **Assertions:**
  - [ ] Error message "[text]" is visible
  - [ ] Record was NOT created

---

## Rules

> These override default behavior for this module.

- If a dropdown has no exact match, pick the closest option and note it in the report
- If a step fails, screenshot and continue to the next test case
- If login is required, use env credentials (never hardcode)
- Reuse existing test data where possible — don't create new records unless the test requires it

---

## Report Structure

> After running, Claude fills this in and saves it to `test-reports/[module]-[date].md`

### Run Summary
| Field          | Value       |
|---------------|-------------|
| Date          | YYYY-MM-DD  |
| Total cases   | N           |
| Passed        | N           |
| Failed        | N           |
| Skipped       | N           |
| Duration      | ~Xm         |

### Results

#### TC-01: [description]
- **Result:** Pass / Fail
- **Notes:** [Any observations]
- **Screenshot:** [filename if captured]

#### TC-02: [description]
- **Result:** Fail
- **Failure reason:** [What went wrong]
- **Actual vs Expected:** [Comparison]
- **Screenshot:** [filename]

### Issues Found
| # | Test Case | Severity | Description              |
|---|-----------|----------|--------------------------|
| 1 | TC-02     | High     | Validation not triggered  |

### Recommendations
- [Actionable suggestions based on findings]
