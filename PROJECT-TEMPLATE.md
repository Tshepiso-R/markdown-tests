# Markdown-Driven Testing — New Project Template

Copy this structure to set up automated E2E testing on any web application.

---

## 0. Starter Prompt

> Paste this into Claude Code to bootstrap a new project. Replace the placeholders with your app details.

```
I want to set up markdown-driven E2E testing for my web application.

App: [YOUR APP NAME]
URL: [YOUR APP URL]
Environment: [QA/Staging/Dev]

Accounts:
- Admin: [username] / [password]
- User: [username] / [password]

The main user journey I want to test is:
[Describe your end-to-end flow, e.g.:
1. Login as admin
2. Create a new [record type]
3. Fill in mandatory fields: [list fields]
4. Submit and verify it appears in the list
5. Open the record and verify all fields saved correctly
6. Perform [workflow action]
7. Verify status changes to [expected status]
]

Test data to reuse (don't create new records with these IDs — they may trigger paid API calls):
- [ID/key 1] — [description]
- [ID/key 2] — [description]

Please:
1. Create the project structure (CLAUDE.md, test-plans/RULES.md, test-plans/TEMPLATE.md)
2. Write the first test plan based on my user journey above
3. Set up GitHub Actions workflow for CI (using Sonnet model, 800 max turns)
4. Set up GitHub Pages dashboard for viewing reports
5. Run the first test locally and generate a report

Use the markdown-driven testing approach:
- Test plans are markdown files in test-plans/
- Claude reads the plan and drives the browser directly via MCP browser tools (snapshot, click, fill, etc.)
- Reports are saved to test-reports/ with pass/fail assertions
- No traditional test scripts — markdown is the source of truth
- Do NOT generate Playwright, Cypress, Selenium, or any other test framework code
- Do NOT write .spec.ts, .test.js, or any script files
- Always read CLAUDE.md and test-plans/RULES.md before executing any test plan
```

---

## 1. Project Structure

```
your-project/
├── .github/
│   ├── workflows/
│   │   ├── e2e-test.yml          ← CI pipeline
│   │   └── deploy-reports.yml    ← GitHub Pages dashboard
│   └── mcp-config.json           ← MCP Playwright config
├── test-plans/
│   ├── RULES.md                  ← Global execution rules
│   ├── TEMPLATE.md               ← Test plan template
│   └── e2e-[scenario].md         ← One per user journey
├── test-reports/
│   └── [scenario]-[date].md      ← Generated after each run
├── azdo-sync/
│   ├── SYNC-PLAYBOOK.md          ← Instructions for syncing to Azure DevOps
│   ├── DRIFT-PLAYBOOK.md         ← Instructions for drift detection
│   └── mapping.json              ← ID mapping: markdown ↔ AzDO work items
├── CLAUDE.md                     ← Project instructions for Claude
└── .gitignore
```

---

## 2. CLAUDE.md

```markdown
# CLAUDE.md – Markdown-Driven Testing

This project uses markdown files to define and execute tests.
No scripts — Claude drives the browser directly from test plan definitions using MCP browser tools.

> **IMPORTANT:** This is NOT a Playwright/Cypress/Selenium project. Do NOT generate test scripts or .spec.ts/.test.js files.
> Claude reads markdown test plans and executes them by driving the browser directly via MCP tools (browser_snapshot, browser_click, browser_fill_form, etc.).

## How It Works
1. Test plans live in `test-plans/` as `.md` files
2. Claude reads a test plan, opens the browser, and executes each test case using MCP browser tools
3. Results are saved to `test-reports/[scenario]-[date].md`

## Running Tests
When asked to run a test plan:
1. Read `CLAUDE.md` (this file) first
2. Read `test-plans/RULES.md` — execution rules that govern every test run
3. Read the target test plan fully before touching the browser
4. Execute each test case using MCP browser tools (snapshot, click, fill, assert)
5. Generate a report in `test-reports/`

## Key Rules
- Never guess — always snapshot the browser before acting
- Never hardcode credentials — use env variables
- On failure: screenshot, note what happened, continue to next test case
- Every assertion must be explicitly checked and marked pass/fail
- Every step must have an expected result — never leave it blank
- Every test case must list its prerequisites
- Reuse existing test data — don't create new records unless required
- NEVER generate Playwright, Cypress, Selenium, or any test framework code

## Azure DevOps Sync
Test plans can be synced to Azure DevOps Test Plans. See `azdo-sync/SYNC-PLAYBOOK.md`.
After every test run, drift detection compares results against the plan. See `azdo-sync/DRIFT-PLAYBOOK.md`.
```

---

## 3. RULES.md

```markdown
# Test Execution Rules

## Before Testing
1. **Read the full test plan** before touching the browser
2. **Check prereqs** — if login is needed, do it first
3. **Navigate to the target URL** and snapshot to confirm
4. **Do not guess** — if the UI doesn't match, stop and report

## During Testing

### Navigation
- Snapshot before every action to see current state
- Never assume a page has loaded — verify with a snapshot

### Filling Forms
- Snapshot after filling each field to confirm the value took
- For dropdowns: snapshot to see options, then select
- Clear existing field values before typing new ones

### Clicking / Submitting
- Snapshot before clicking to confirm the target is visible
- Snapshot after clicking to verify the outcome
- Every click has a consequence — note what happened (dialog opened, toast appeared, page redirected)

## Assertions
- Mark each assertion: `[x]` for pass, `[!]` for fail
- Never skip assertions — every one must be evaluated

## On Failure
1. Screenshot the current state
2. Note the exact step that failed
3. Note expected vs actual
4. Continue to the next test case

## Step Execution — Zero Tolerance for Skipping
- Execute EVERY step in order, one at a time
- Never jump ahead to a final action before completing all preceding steps
- A test case with skipped steps is a FAIL, not a PASS

## Test Data
> List approved test data here to avoid creating costly records.

| Person | ID/Key | Use For |
|--------|--------|---------|
| [Name] | [ID]   | [Role]  |

## After Testing
1. Save report to `test-reports/[module]-YYYY-MM-DDTHH-MM.md`
2. Summarize: total pass/fail/skip, issues, recommendations
3. Run drift detection — compare report against test plan (see azdo-sync/DRIFT-PLAYBOOK.md)
4. If changes detected, add "Changes Detected" section to report with suggested updates

## What NOT to Do
- Do NOT hardcode credentials in reports
- Do NOT create records unless the test requires it
- Do NOT skip steps within a test case
- Do NOT modify the test plan during execution
```

---

## 4. Test Plan Template 

```markdown
# Test Plan: [Feature Name]

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
| Field        | Value                          |
|-------------|--------------------------------|
| Module      | [Feature or user journey]       |
| URL         | [Base URL]                      |
| Prereqs     | [Login required? Data needed?]  |
| Last tested | YYYY-MM-DD                      |
| Status      | Not yet tested                  |

---

## Accounts Used
| Role | Username | Password | Used In |
|------|----------|----------|---------|
| Admin | [user] | [env var] | TC-01, TC-02 |
| User  | [user] | [env var] | TC-03+ |

---

## TC-01: [Happy path description]
- **Type:** Happy path
- **Login:** [account]
- **Prerequisites:** None — first step in the journey
- **URL:** [starting page]
- **Steps:**
  1. Navigate to [page] → _Page loads with [expected content]_
  2. Click [button] → _[Dialog opens / form loads / toast appears]_
  3. Fill [field] with [value] → _Field accepts value_
  4. Click [submit] → _[Dialog closes / form saves / page redirects]_
- **Input data:**
  | Field | Value | Type |
  |-------|-------|------|
  | Name  | Test  | Text |
- **Expected result:** [What should happen]
- **Assertions:**
  - [ ] [Thing to verify]
  - [ ] [Another thing]

> **Rule:** Every step must describe what should happen after the action. Never leave expected results blank — if clicking a button closes a dialog, say "Dialog closes". If clicking Save shows a toast, say what the toast should say.

---

## TC-02: [Negative test description]
- **Type:** Negative
- **Prerequisites:** TC-01 passed — [record] exists with status "[status]"
- **Steps:**
  1. Leave [required field] empty
  2. Click submit → _System blocks submission and shows error_
- **Expected result:** Validation error shown
- **Assertions:**
  - [ ] Error message: "[exact error text]"
  - [ ] Record NOT created
  - [ ] Status remains unchanged

---

## TC-03: [Edge case description]
- **Type:** Edge case
- **Prerequisites:** [What state/data must exist before this test case]
- **Steps:**
  1. [Unusual action] → _[What should happen]_
- **Expected result:** [Expected behavior]
- **Assertions:**
  - [ ] [Verification]
```

---

## 5. GitHub Actions Workflow

```yaml
name: E2E Tests

on:
  workflow_dispatch:
    inputs:
      test_plan:
        description: "Test plan to execute"
        type: choice
        options:
          - e2e-[your-feature]
  schedule:
    - cron: "0 0 * * *"

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    permissions:
      contents: write
      id-token: write

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npx playwright install chromium --with-deps

      - name: Set report name
        id: report
        run: |
          PREFIX=${{ github.event_name == 'schedule' && 'scheduled' || 'manual' }}
          NAME="${{ inputs.test_plan || 'e2e-your-feature' }}-${PREFIX}-$(date +%Y-%m-%dT%H-%M)"
          echo "name=${NAME}" >> $GITHUB_OUTPUT

      - name: Run tests
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            E2E test. Run ID: ${{ github.run_id }}. BE EFFICIENT.
            1. Read test-plans/RULES.md then test-plans/${{ inputs.test_plan || 'e2e-your-feature' }}.md
            2. Execute ALL test cases sequentially.
            3. Save report to test-reports/${{ steps.report.outputs.name }}.md
            4. Each TC: URL + pass/fail. No screenshots.
            5. Print RESULT: PASS or RESULT: FAIL
            Environment: [YOUR_APP_URL]
            Credentials: ${{ secrets.USERNAME }} / ${{ secrets.PASSWORD }}
            [YOUR TEST DATA / RULES HERE]
          claude_args: "--max-turns 800 --model sonnet --dangerously-skip-permissions --mcp-config .github/mcp-config.json"
        env:
          APP_PASSWORD: ${{ secrets.APP_PASSWORD }}

      - name: Post report to summary
        if: always()
        run: |
          REPORT="test-reports/${{ steps.report.outputs.name }}.md"
          if [ -f "$REPORT" ]; then
            echo "## ${{ steps.report.outputs.name }}" >> $GITHUB_STEP_SUMMARY
            cat "$REPORT" >> $GITHUB_STEP_SUMMARY
          fi

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-report
          path: test-reports/

      - name: Commit report
        if: success()
        run: |
          git config user.email "github-actions@github.com"
          git config user.name "GitHub Actions"
          git pull --rebase origin main || true
          git add test-reports/*.md 2>/dev/null || true
          git diff --cached --quiet || git commit -m "CI: ${{ steps.report.outputs.name }}"
          git push || true
```

---

## 6. MCP Config

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp", "--headless"]
    }
  }
}
```

---

## 7. .gitignore

```
.playwright-mcp/
*.png
*.jpeg
!test-reports/screenshots/**/*.png
!test-reports/screenshots/**/*.jpeg
```

---

## 8. GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Claude API key |
| `APP_PASSWORD` | Your app's test account password |
| `AZDO_PAT` | Azure DevOps Personal Access Token (optional — for Test Plans sync) |

---

## 9. Azure DevOps Integration (Optional)

If your team uses Azure DevOps Test Plans for test management:

1. **Create a PAT** in Azure DevOps with these scopes:
   - Test Management: Read & Write
   - Work Items: Read & Write
2. **Add `AZDO_PAT`** to your GitHub Secrets (for CI) and/or set as a local environment variable
3. **Configure your org/project** in `azdo-sync/SYNC-PLAYBOOK.md` — update the Configuration table at the top
4. **Sync a test plan:** Ask Claude "Sync test-plans/[your-plan].md to Azure DevOps"
5. **Drift detection** runs automatically after every test execution — see reports for "Changes Detected" section

The mapping between markdown test cases and AzDO work items is stored in `azdo-sync/mapping.json`.

---

## 10. Setup Checklist

- [ ] Copy project structure
- [ ] Update CLAUDE.md with your app details
- [ ] Update RULES.md with your test data
- [ ] Write your first test plan in `test-plans/`
- [ ] Create GitHub repo and push
- [ ] Install Claude Code GitHub App: https://github.com/apps/claude
- [ ] Set secrets in repo settings
- [ ] Enable GitHub Pages (Settings > Pages > Source: GitHub Actions)
- [ ] Run first test: Actions > Run workflow
- [ ] (Optional) Set up Azure DevOps integration — see section 9

---

## Estimated Costs (Sonnet)

| Turns | ~USD | ~ZAR |
|-------|------|------|
| 200 (simple flow) | $1.50 | R28 |
| 400 (complex flow) | $3.00 | R56 |
| 800 (large suite) | $6.00 | R111 |
| Daily (3 plans) | $9/day | R167/day |
| Monthly (weekdays) | $190/mo | R3,500/mo |
