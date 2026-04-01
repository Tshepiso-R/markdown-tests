# Onboarding — Markdown-Driven Testing

Welcome to the team. This document explains how our testing setup works and how to get started.

---

## The Concept

Test plans are written in **markdown files** — no Playwright, Cypress, or Selenium scripts. Claude reads the markdown, opens a browser, executes each step, and generates a report.

---

## Project Structure

```
test-plans/
  RULES.md                 ← Rules Claude follows during every test run
  TEMPLATE.md              ← Copy this to write new test plans
  e2e-[scenario].md        ← One file per user journey

test-reports/
  [module]/[report].md     ← Generated after each run (timestamped)
  screenshots/[module]/    ← Screenshots from test runs

azdo-sync/
  SYNC-PLAYBOOK.md         ← Instructions to sync test plans → Azure DevOps Test Plans
  DRIFT-PLAYBOOK.md        ← Detects when the app changed vs what the plan expects
  mapping.json             ← Links markdown test cases to AzDO work item IDs
```

---

## How a Test Plan is Structured

Each test plan has:

1. **Meta** — module name, URL, prerequisites, test data
2. **Phases** — logical groups (e.g., Phase 1: Lead Capture, Phase 2: Pre-Screening)
3. **Test Cases (TC-XX)** inside each phase, with:
   - **Type** — Happy path / Negative / Edge case
   - **Prerequisites** — what must be true before this TC runs (e.g., "TC-01 passed, lead exists")
   - **Login** — which account to use
   - **Steps** — numbered actions, each with an expected result (never blank)
   - **Input data** — table of fields/values
   - **Expected result** — what should happen overall
   - **Assertions** — checkboxes that get marked pass `[x]` or fail `[!]`

### Example Test Case

```markdown
### TC-01: Create Individual lead
- **Type:** Happy path
- **Login:** admin
- **Prerequisites:** None — first step in the journey
- **Steps:**
  1. Navigate to Leads table via sidebar menu → Leads table loads
  2. Click "New Lead" → Lead creation dialog opens
  3. Fill all required fields → Fields accept values without errors
  4. Click OK → Dialog closes, lead saved, returns to Leads table
- **Input data:**
  | Field | Value | Type |
  |-------|-------|------|
  | First Name | IanTest123 | Text |
  | Client Type | Individual | Dropdown |
- **Expected result:** Lead created with status "New"
- **Assertions:**
  - [ ] Lead appears at top of Leads table
  - [ ] Lead status: "New"
  - [ ] All fields saved correctly
```

---

## How to Run a Test

### Locally

Open Claude Code in this repo and say:

```
Run the personal loan E2E test plan
```

Claude will:
1. Read `test-plans/RULES.md` first (mandatory)
2. Read the target test plan fully
3. Open the browser, navigate via sidebar menu (never direct URLs)
4. Snapshot before and after every action
5. Fill forms, click buttons, assert results
6. Generate a timestamped report in `test-reports/`
7. Run **drift detection** — flag if the app changed since the plan was written

### Via CI

GitHub Actions runs nightly or on manual dispatch (Actions tab → Run workflow). Uses `anthropics/claude-code-action` with headless Playwright MCP. Reports are committed back to the repo and uploaded as artifacts.

---

## Azure DevOps Integration

Test plans sync to Azure DevOps Test Plans for centralized test management:

| Markdown | Azure DevOps |
|----------|-------------|
| 1 `.md` file | 1 Test Plan |
| `## PHASE N: Name` | 1 Test Suite |
| `### TC-XX: Description` | 1 Test Case (with steps + expected results + prerequisites) |

### Commands

- **Sync a plan:** "Sync test-plans/[plan].md to Azure DevOps"
- **Re-sync after edits:** "Re-sync [plan] to Azure DevOps"
- **Drift detection:** Runs automatically after every test execution

The mapping between markdown and AzDO work items is stored in `azdo-sync/mapping.json`.

---

## Drift Detection

After every test run, Claude compares what the test plan expected vs what actually happened. If the app changed (button renamed, toast message different, field removed), the report includes a **"Changes Detected"** section with:

- A table of what changed and its severity (High / Medium / Low)
- Suggested updates to the test plan
- Whether to update the plan or file a bug — **the team decides, not Claude**

---

## Key Rules

| Rule | Why |
|------|-----|
| Never skip steps | A prior run falsely passed by skipping 5 verification steps |
| Never leave expected results blank | Every click has a consequence — document it |
| Every TC needs prerequisites | So anyone knows what state is required before running it |
| Reuse approved test IDs | New SA ID numbers trigger paid verification API calls |
| Use testmail.app for emails | Real inboxes can't be queried programmatically |
| Navigate via sidebar | Never paste URLs directly — test like a real user |
| Assert toasts + status badges | After every state-changing action |
| Edit all tabs, save once | Don't save between Client Info and Loan Info tabs |
| Don't auto-fix drift | Report flags changes, team decides whether to update or file a bug |
| Never use browser_evaluate for UI | Only use browser_snapshot + MCP actions |

---

## Writing a New Test Plan

1. Copy `test-plans/TEMPLATE.md`
2. Fill in **Meta** — module, URL, accounts, test data
3. Define **Phases** — group test cases by workflow stages
4. Write **Test Cases** — for each one:
   - List prerequisites (which prior TCs must pass, what state is needed)
   - Write steps with expected results after every action
   - Add input data tables for form fields
   - Add assertions as checkboxes
5. Add **module-specific rules** if the module has special behavior
6. Sync to Azure DevOps: "Sync test-plans/[your-plan].md to Azure DevOps"

### Step Expected Results — Examples

Every step must describe what happens. Never leave it blank:

| Action | Expected Result |
|--------|----------------|
| Click "New Lead" | Lead creation dialog opens |
| Click OK | Dialog closes, lead saved, returns to table |
| Click Edit | Form switches to edit mode, fields become editable |
| Click Save | Form returns to read-only mode, toast: "Data saved successfully!" |
| Click "Initiate Loan Application" | Processing indicator appears, toast confirms submission |
| Click "Request OTP" | Toast: "The one-time-password (OTP) has been sent" |
| Click "Finalise Verification Outcomes" | Verification finalised, page redirects to next workflow step |

---

## Test Data

These IDs are shared across all test plans. **Never generate new ones** — each new ID triggers a paid verification API call.

| Person | ID Number | Role |
|--------|-----------|------|
| Ian Houvet | 7708206169188 | Personal applicant, Entity director (Married) |
| Chamaine Houvet | 7304190225085 | Entity director, Spouse of Ian |
| Xolile Ndlangana | 6311115651080 | Entity director |

**Entity:** Boxfusion, Registration: 2012/225386/07

**Emails:** All emails use testmail.app — `5s9ku.[tag]@inbox.testmail.app`. Never use personal or company email addresses.

---

## Secrets Required

| Secret | Where | Description |
|--------|-------|-------------|
| `ANTHROPIC_API_KEY` | GitHub Secrets | Claude API key for CI runs |
| `ADMIN_PASSWORD` | GitHub Secrets | Admin account password |
| `RM_PASSWORD` | GitHub Secrets | RM (Fatima) account password |
| `TESTMAIL_API_KEY` | GitHub Secrets | Testmail.app API key for consent/OTP emails |
| `AZDO_PAT` | GitHub Secrets + local env | Azure DevOps PAT for Test Plans sync |

---

## Quick Reference

| I want to... | Do this |
|--------------|---------|
| Run a test locally | "Run the [plan name] test plan" |
| Run a test via CI | Actions tab → Run workflow |
| Write a new test plan | Copy `test-plans/TEMPLATE.md`, fill it in |
| Sync to Azure DevOps | "Sync test-plans/[plan].md to Azure DevOps" |
| Check what changed | Look for "Changes Detected" section in the latest report |
| Update a plan after drift | Review suggested updates in the report, apply manually |
| See execution rules | Read `test-plans/RULES.md` |
| See project config | Read `CLAUDE.md` |
