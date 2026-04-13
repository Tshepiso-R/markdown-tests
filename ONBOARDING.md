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

**Emails:** All emails use testmail.app — `guwn6.[tag]@inbox.testmail.app`. Never use personal or company email addresses.

---

## Secrets Required

| Secret | Where | Description |
|--------|-------|-------------|
| `ANTHROPIC_API_KEY` | GitHub Secrets | Claude API key for CI runs |
| `ADMIN_PASSWORD` | GitHub Secrets | Admin account password |
| `RM_PASSWORD` | GitHub Secrets | RM (Fatima) account password |
| `TESTMAIL_API_KEY` | GitHub Secrets | Testmail.app API key for consent/OTP emails |
| `AZDO_PAT` | GitHub Secrets + local env | Azure DevOps PAT for Test Plans sync |
| `TEAMS_WEBHOOK_URL` | GitHub Secrets | Microsoft Teams Incoming Webhook for CI notifications |

---

## Teams Notifications

After every CI run (pass or fail), a notification is posted to Microsoft Teams with the result, summary counts, and links to the run and report.

### How to Set Up the Webhook

1. In Microsoft Teams, go to the channel where you want notifications
2. Click the **...** menu on the channel → **Connectors** (or **Manage channel** → **Connectors**)
3. Find **Incoming Webhook** → click **Configure**
4. Give it a name (e.g., "E2E Test Results") and optionally upload an icon
5. Click **Create** → copy the webhook URL
6. Add it as a GitHub Secret:
   - Go to your repo → **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `TEAMS_WEBHOOK_URL`
   - Value: paste the webhook URL
7. Done — next CI run will post to your channel

### What the Notification Looks Like

The card shows:
- **Result:** PASS or FAIL (with icon)
- **Trigger:** scheduled or manual
- **Date:** when it ran
- **Summary:** X total | Y passed | Z failed
- **Buttons:** "View Run" (GitHub Actions) and "View Report" (markdown report)

If the webhook secret is not configured, the step silently skips — it won't break the pipeline.

---

## Azure DevOps Personal Access Token (PAT)

A PAT is needed to sync test plans to Azure DevOps. Each team member who wants to run syncs locally needs their own.

### How to Create a PAT

1. Go to **Azure DevOps** → click your profile icon (top right) → **Personal access tokens**
   - Or navigate directly to: `https://dev.azure.com/boxfusion/_usersSettings/tokens`
2. Click **+ New Token**
3. Configure:
   - **Name:** Something descriptive (e.g., "Markdown Test Sync")
   - **Organization:** `boxfusion`
   - **Expiration:** Choose a duration (max 1 year)
   - **Scopes:** Select **Custom defined**, then enable:
     - **Test Management** → Read & Write
     - **Work Items** → Read & Write
4. Click **Create** and **copy the token immediately** — you won't see it again
5. Set it as an environment variable locally:
   ```bash
   export AZDO_PAT="your-token-here"
   ```
   Or on Windows (PowerShell):
   ```powershell
   $env:AZDO_PAT = "your-token-here"
   ```

### For CI

The PAT is stored as a GitHub Secret (`AZDO_PAT`). Only repo admins can update it. If the token expires, CI syncs will fail — regenerate and update the secret.

---

## Testmail.app — How It Works

The loan application workflow sends emails for **consent** and **OTP verification**. We can't use real email inboxes because Claude needs to programmatically read these emails during test runs. Testmail.app solves this.

### What Is It

Testmail.app provides disposable email inboxes that can be queried via API. Every email sent to `guwn6.[anything]@inbox.testmail.app` lands in our namespace and can be retrieved by tag.

### How the Email Address Works

```
guwn6.consent-1234567890@inbox.testmail.app
│     │       │
│     │       └─ Unique identifier (timestamp or run ID)
│     └─ Tag — used to filter emails in the API
└─ Namespace — our testmail.app account
```

- The **namespace** (`guwn6`) is fixed — it's our account
- The **tag** is everything between the dot and the `@` — used to isolate emails per test run
- Each test run uses a **unique tag** (e.g., `consent-1712000000`) so emails from different runs don't collide

### When Emails Are Sent

| Trigger | Email Subject | Sent To |
|---------|--------------|---------|
| Initiate Loan (Personal) | "Action Required: Provide Consent" | Lead's email address |
| Initiate Loan (Entity) | "Action Required: Company Resolution Needed" | Each director's email |
| After all directors sign resolution | "Action Required: Provide Consent" | Contact Person's email |
| Click "Request OTP" on consent/resolution page | "One-Time-Pin" | Same address |

### How Claude Retrieves Emails

Claude calls the testmail.app API to check for incoming emails:

```
GET https://api.testmail.app/api/json
  ?apikey={TESTMAIL_API_KEY}
  &namespace=guwn6
  &tag={tag}
  &livequery=true
  &timeout=60000
```

- **`livequery=true`** — waits for the email to arrive (long-polling, up to 60 seconds)
- **`tag`** — filters to only emails for this test run
- **`timeout=60000`** — waits up to 60 seconds before giving up

The response includes the email body as HTML. Claude extracts:
- **Consent/resolution URL** — the link the applicant/director clicks to sign
- **OTP code** — extracted with regex: `Your One-Time-Pin is (\d+)`

### Example Flow (Personal Loan Consent)

1. Claude initiates the loan → app sends consent email to `guwn6.consent-run123@inbox.testmail.app`
2. Claude calls testmail.app API with `tag=consent-run123`
3. API returns the email → Claude extracts the consent URL
4. Claude opens the URL in the browser → clicks "Request OTP"
5. App sends OTP email to the same address
6. Claude calls API again (with `timestamp_from` to get only new emails) → extracts OTP
7. Claude enters OTP → signs consent → done

### Why Not Real Emails

- Personal/company inboxes can't be queried via API
- Shared inboxes would mix emails from different test runs
- Testmail.app isolates emails by tag — each run sees only its own emails
- It's free for our usage volume

### Account Details

| Field | Value |
|-------|-------|
| Service | testmail.app |
| Namespace | `guwn6` |
| API Key | Stored in GitHub Secrets as `TESTMAIL_API_KEY` |
| Email format | `guwn6.{tag}@inbox.testmail.app` |
| Dashboard | Log in at testmail.app to see all received emails |

---

## How to Contribute

### Adding a Test Case to an Existing Plan

1. Open the test plan file (e.g., `test-plans/e2e-personal-loan-application.md`)
2. Find the Phase where your test case belongs
3. Add a new `### TC-XX:` section following the format:
   - **Type** — Happy path, Negative, or Edge case
   - **Prerequisites** — what must be true before this runs (which TCs must pass, what data/state exists)
   - **Login** — which account
   - **Steps** — numbered, with expected result after every action (e.g., `Click Save → Form returns to read-only mode`)
   - **Input data** — table of fields, values, and types
   - **Expected result** — overall outcome
   - **Assertions** — checkboxes for each thing to verify
4. Commit and push
5. Re-sync to AzDO: "Re-sync [plan] to Azure DevOps"

### Creating a New Test Plan

1. Copy `test-plans/TEMPLATE.md` → `test-plans/e2e-[your-scenario].md`
2. Fill in all sections:
   - **Meta** — module, URL, accounts, test data
   - **User Journey Overview** — tree diagram of the full flow
   - **Accounts Used** — table of roles and credentials (use env vars, never hardcode passwords)
   - **Phases** — group test cases by workflow stage
   - **Test Cases** — follow the format above
   - **Rules** — any module-specific rules that override or extend RULES.md
3. Review with the team before first run
4. Sync to AzDO: "Sync test-plans/[your-plan].md to Azure DevOps"
5. Add to CI workflow in `.github/workflows/e2e-test.yml` if it should run nightly

### Updating a Test Plan After Drift

When a test report flags changes in the "Changes Detected" section:

1. Read the drift report — it lists what changed and suggests specific edits
2. **If the change is intentional** (app was updated): apply the suggested edits to the test plan
3. **If the change is unexpected** (possible bug): file a bug instead of updating the plan
4. After updating, re-sync to AzDO to keep both in sync
5. Commit with a message like: "Update [plan] — [what changed] (drift from [report date])"

### Contribution Checklist

- [ ] Every step has an expected result (never blank)
- [ ] Every test case has prerequisites listed
- [ ] Test data uses approved IDs from RULES.md (never new ones)
- [ ] Emails use testmail.app addresses (never personal/company emails)
- [ ] Negative tests assert the exact error message text
- [ ] Assertions include toast messages and status badge values
- [ ] No hardcoded credentials anywhere
- [ ] Test plan reads correctly without needing to run it (someone should understand the flow just by reading)

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
