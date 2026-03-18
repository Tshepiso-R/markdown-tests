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
- Always use approved test IDs from RULES.md — never generate new ones

---

## Report Structure

> After running, Claude fills this in and saves to `test-reports/[module]-YYYY-MM-DDTHH-MM.md`
> Screenshots saved to `test-reports/screenshots/[report-name]/`

### Run Summary
| Field          | Value       |
|---------------|-------------|
| Date          | YYYY-MM-DD  |
| Time          | HH:MM UTC   |
| Total cases   | N           |
| Passed        | N           |
| Failed        | N           |
| Skipped       | N           |
| Duration      | ~Xm         |

### Results

#### TC-01: [description]
- **URL:** `https://landbankcrm-adminportal-qa.shesha.app/dynamic/...`
- **Result:** Pass / Fail
- **Notes:** [Any observations]

##### Steps Followed
1. [Step with URL visited]
2. [Step with action taken]

##### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Lead form](../screenshots/report-name/tc01-form.png) | Lead creation form filled |
| ![Lead saved](../screenshots/report-name/tc01-saved.png) | Lead saved in table |

##### Input vs Output
| Field | Submitted | Returned | Match |
|-------|-----------|----------|-------|
| First Name | Test | Test | YES |

#### TC-02: [description]
- **URL:** `https://landbankcrm-adminportal-qa.shesha.app/dynamic/...`
- **Result:** Fail
- **Failure reason:** [What went wrong]
- **Actual vs Expected:** [Comparison]

##### Snapshots
| Screenshot | Description |
|-----------|-------------|
| ![Error](../screenshots/report-name/tc02-error.png) | Validation error shown |

### Issues Found
| # | Test Case | Severity | Description              |
|---|-----------|----------|--------------------------|
| 1 | TC-02     | High     | Validation not triggered  |

### UX / UI Observations
| # | Page | Type | Description | Recommendation |
|---|------|------|-------------|---------------|
| 1 | Lead Detail | UX | "No image available" text is easy to miss | Add bordered placeholder with icon |

### Recommendations
- [Actionable suggestions based on findings]

### Time Elapsed
- Start: HH:MM
- End: HH:MM
- Duration: Xm
