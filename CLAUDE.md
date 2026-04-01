# CLAUDE.md – Markdown-Driven Testing

This project uses markdown files to define and execute tests. No scripts — Claude drives the browser directly from test plan definitions.

---

## How It Works

1. Test plans live in `test-plans/` as `.md` files
2. Claude reads a test plan, opens the browser, and executes each test case
3. Results are saved to `test-reports/[scenario]-[date].md`

---

## Project Structure

```
test-plans/
  TEMPLATE.md              ← copy this to create new test plans
  RULES.md                 ← global execution rules (always read before running)
  e2e-[scenario].md        ← one test plan per end-to-end user journey
test-reports/
  [scenario]-YYYY-MM-DD.md ← generated after each run
azdo-sync/
  SYNC-PLAYBOOK.md         ← instructions for syncing test plans to Azure DevOps
  DRIFT-PLAYBOOK.md        ← instructions for detecting changes after test runs
  mapping.json             ← ID mapping between markdown test cases and AzDO work items
reporting/
  SETUP.md                 ← full setup instructions for all reporting tools
  convert-to-allure.py     ← markdown → Allure HTML reports
  collect-metrics.py        ← markdown → JSON metrics for Grafana
  flaky-monitor.py          ← detects tests that flip between pass/fail
  duration-tracker.py       ← execution time trends and slow-run alerts
  failure-heatmap.py        ← failure frequency by TC, phase, and module
  drift-history.py          ← correlates plan edits with test failures
  coverage-gaps.py          ← finds untested app features
  report-completeness.py    ← enforces RULES.md quality standards
  stale-plans.py            ← flags plans not run in X days
  cost-report.py            ← tracks verification API costs per run
  metrics/                  ← generated reports (md + json)
  allure-results/           ← generated Allure JSON
  grafana/                  ← Grafana dashboard config
```

---

## Running Tests

When asked to run a test plan:

1. Read `test-plans/RULES.md` first
2. Read the target test plan
3. Execute each test case using browser tools (snapshot, click, fill, assert)
4. Generate a report in `test-reports/`
5. Run reporting suite: `py reporting/collect-metrics.py && py reporting/flaky-monitor.py && py reporting/cost-report.py`

---

## Reporting Suite

After test runs, generate analysis reports from `reporting/`:

```bash
# Run all analysis tools
py reporting/collect-metrics.py        # metrics JSON for Grafana
py reporting/convert-to-allure.py --all # Allure HTML reports
py reporting/flaky-monitor.py          # flaky test detection
py reporting/duration-tracker.py       # execution time trends
py reporting/failure-heatmap.py        # failure frequency
py reporting/drift-history.py          # plan edit vs failure correlation
py reporting/coverage-gaps.py          # untested features
py reporting/report-completeness.py    # report quality scores
py reporting/stale-plans.py            # stale plan alerts
py reporting/cost-report.py            # verification API costs
```

Full setup instructions: `reporting/SETUP.md`

---

## Writing Test Plans

1. Copy `test-plans/TEMPLATE.md`
2. Fill in Meta, Flow, Test Cases, and any module-specific Rules
3. Each test case must have: type, prerequisites, steps, expected result, and assertions
4. Every step must describe what should happen — never leave expected results blank
5. Every test case must list its prerequisites (which prior TCs must pass, what state is needed)

---

## Key Rules

- Never guess — always snapshot the browser before acting
- Never hardcode credentials — use env variables
- On failure: screenshot, note what happened, continue to next test case
- Every assertion must be explicitly checked and marked pass/fail
- Reuse existing test data — don't create new records unless required

---

## Azure DevOps Sync

Test plans are synced to Azure DevOps Test Plans for centralized test management. Each PHASE becomes a Test Suite, each TC becomes a Test Case with action steps, expected results, and validation steps.

- **Sync instructions:** Read `azdo-sync/SYNC-PLAYBOOK.md`
- **Drift detection:** Read `azdo-sync/DRIFT-PLAYBOOK.md`
- **Mapping file:** `azdo-sync/mapping.json` — stores the IDs linking markdown to AzDO
- **Required secret:** `AZDO_PAT` environment variable (Azure DevOps Personal Access Token)

### Commands

- **Sync a plan:** "Sync test-plans/[plan].md to Azure DevOps"
- **Re-sync after updates:** "Re-sync [plan] to Azure DevOps" (PATCHes only changed items)
- **Drift detection:** Runs automatically after every test run (see RULES.md)

### AzDO Test Case Format

When syncing, every step (action or validation) must have an expected result:
- **Action steps:** Describe what should happen — dialog opens, form loads, toast appears, page redirects
- **Validation steps:** Describe the expected state — specific toast text, status badge value, field content
- **Never leave expected results blank** — if clicking OK closes a dialog, say "Dialog closes"
- **Prerequisites** are included in the test case description — which prior TCs must pass and what state is required
