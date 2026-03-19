# Markdown-Driven E2E Testing

Automated end-to-end testing for the LandBank CRM loan application workflow, driven entirely from markdown test plans. Claude reads the test plans, opens a browser, executes each test case, and generates reports.

---

## How It Works

1. **Test plans** define the steps, input data, and expected results in markdown
2. **Claude** reads a test plan, opens the browser, and executes each test case
3. **Results** are saved as markdown reports with screenshots

No test scripts, no test framework — just markdown and a browser.

---

## Project Structure

```
markdown-tests/
  CLAUDE.md                          # Project instructions for Claude
  README.md                          # This file
  test-plans/
    TEMPLATE.md                      # Copy this to create new test plans
    RULES.md                         # Execution rules (read before every run)
    e2e-personal-loan-application.md # Personal loan: Lead -> Workflow -> Complete
    e2e-entity-loan-application.md   # Entity loan: Lead -> Resolution -> Consent -> Complete
    e2e-negative-edge-cases.md       # Negative/edge case scenarios
  test-reports/
    personal-loan/                   # Personal loan run reports
      personal-loan-YYYY-MM-DDTHH-MM.md
      ...
    entity-loan/                     # Entity loan run reports
      entity-loan-YYYY-MM-DDTHH-MM.md
      ...
    negative-edge-cases/             # Negative test run reports
    screenshots/
      personal-loan/                 # Screenshots from personal loan runs
      entity-loan/                   # Screenshots from entity loan runs
      negative-edge-cases/           # Screenshots from negative test runs
```

---

## Test Plans

### Personal Loan (Individual)
**File:** `test-plans/e2e-personal-loan-application.md`

Full journey for an individual loan application:
- TC-01: Create Individual lead
- TC-02: Pre-screening (7 questions)
- TC-03: Edit Client Info (ID, countries, address, marital status)
- TC-04: Fill Loan Info (product, amount, purpose)
- TC-05: Initiate Loan Application -> Consent Pending
- TC-05c: Consent flow via email (testmail.app OTP)
- TC-06: Review & finalise verification (ID + KYC for applicant + spouse if married)
- TC-07: Complete onboarding checklist -> Workflow COMPLETED

### Entity Loan (Close Corporation)
**File:** `test-plans/e2e-entity-loan-application.md`

Full journey for an entity (Close Corporation) loan application:
- TC-01: Create Close Corporation lead
- TC-02: Pre-screening
- TC-03: Edit Entity Info + Loan Info (single save session)
- TC-03a: Add 3 Directors (with marital details + spouse)
- TC-03b: Add Signatory
- TC-04: Fill Loan Info
- TC-05: Initiate -> Resolution Pending
- TC-05r: ALL directors sign company resolution via email
- TC-05c: Contact person signs consent via email
- TC-06: Review verification (CIPC + all directors + spouses)
- TC-07: Complete onboarding checklist -> Workflow COMPLETED

**Key difference from personal:** Entity flow has a Resolution step where ALL directors must sign before consent can proceed.

### Negative / Edge Cases
**File:** `test-plans/e2e-negative-edge-cases.md`

Validation and error handling scenarios.

---

## Running Tests

### Prerequisites
- Admin account: `admin` / `123qwe`
- RM account: `fatima.abrahams@landbank.co.za` / `123qwe`
- Environment: `landbankcrm-adminportal-qa.shesha.app`

### To run a test plan

Ask Claude:
```
Run the personal loan E2E test plan
```

Claude will:
1. Read `test-plans/RULES.md` first
2. Read the target test plan
3. Open the browser and execute each test case
4. Generate a report in `test-reports/[module]/`

### Test Data

| Person | ID Number | Role |
|--------|-----------|------|
| Ian Houvet | 7708206169188 | Personal applicant, Entity director (Married) |
| Chamaine Houvet | 7304190225085 | Entity director, Spouse of Ian |
| Xolile Ndlangana | 6311115651080 | Entity director |

**Entity:** Boxfusion, Registration: 2012/225386/07

**Email:** All emails use testmail.app (`5s9ku.[tag]@inbox.testmail.app`) for programmatic consent/OTP retrieval.

---

## Key Rules

- **Never skip steps** — every step must be executed and asserted
- **Never use browser_evaluate for UI interaction** — snapshot only
- **Navigate via sidebar menu** — never paste URLs directly
- **Assert all tabs on detail views** — Client Info, Loan Info, Farms
- **Assert toasts and status badges** after every state change
- **Edit all tabs in one save** — don't save between Client Info and Loan Info
- **Reuse test IDs** — new ID numbers cost money (paid verification API)
- **Verify spouses** — if married in community of property, spouse must appear in verifications
- **All director emails must use testmail.app** — required for automated resolution signing

---

## Status Lifecycle

### Personal Loan
```
Lead (New) -> Converted -> Opportunity (Draft) -> Consent Pending
-> Verification In Progress -> Complete
```

### Entity Loan
```
Lead (New) -> Converted -> Opportunity (Draft) -> Resolution Pending
-> Consent Pending -> Verification In Progress -> Complete
```

---

## Report Format

Reports are saved as:
```
test-reports/[module]/[module]-YYYY-MM-DDTHH-MM.md
```

Screenshots are saved as:
```
test-reports/screenshots/[module]/tc01-description.png
```

Each report includes: summary table, per-TC steps followed, assertions with pass/fail checkboxes, URLs, and flagged issues.

---

## Pros and Cons

### Pros

- **No code to maintain** — test plans are plain markdown. Anyone can read, write, or review them without knowing a programming language or test framework.
- **Self-documenting** — the test plan IS the documentation. No gap between what's documented and what's tested.
- **Detailed reports** — every run produces a timestamped report with exact steps, assertions, screenshots, and URLs. Full audit trail.
- **Adapts to UI changes** — Claude reads the actual page state via snapshots before every action. If a button moves or a label changes, it adjusts. No brittle CSS selectors to fix.
- **Catches real issues** — tests run through the real browser like a user would. Finds bugs that unit tests and API tests miss (e.g. the "Awaiting Review" button label not updating).
- **Fast to create new tests** — copy TEMPLATE.md, fill in the steps and expected results. No page objects, no fixtures, no boilerplate.
- **End-to-end coverage including external services** — consent flow, email OTP, third-party verification APIs are all tested in the real flow.
- **Human-readable failures** — when something fails, the report says exactly what happened in plain English with a screenshot. No stack traces to decode.

### Cons

- **Slow execution** — each run takes 15-30 minutes because Claude navigates the browser step by step. Traditional Playwright scripts would be faster.
- **LLM cost per run** — every execution consumes API tokens. Running this on every commit is expensive compared to traditional test suites.
- **Non-deterministic** — Claude may interact with the UI slightly differently between runs (e.g. different click timing, different dropdown selection approach). This can cause flaky results.
- **No parallel execution** — runs are sequential. Can't split test cases across multiple browsers or workers.
- **Limited to what the browser shows** — can't assert database state, API response payloads, or background jobs directly. Only verifies what's visible in the UI.
- **Context window pressure** — long test runs accumulate large snapshots. Late test cases may lose context from early ones as the conversation compresses.
- **Dependent on LLM judgment** — if Claude misinterprets a snapshot or makes a wrong assumption, it may pass a test that should fail (or vice versa). Requires human review of reports.
- **No CI caching or incremental runs** — every run starts from scratch. Can't skip unchanged test cases like traditional test frameworks.
