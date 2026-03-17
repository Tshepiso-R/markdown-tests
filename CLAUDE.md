# CLAUDE.md – Markdown-Driven Testing

This project uses markdown files to define and execute tests. No scripts — Claude drives the browser directly from test plan definitions.

---

## How It Works

1. Test plans live in `test-plans/` as `.md` files
2. Claude reads a test plan, opens the browser, and executes each test case
3. Results are saved to `test-reports/[module]-[date].md`

---

## Project Structure

```
test-plans/
  TEMPLATE.md              ← copy this to create new test plans
  RULES.md                 ← global execution rules (always read before running)
  e2e-[scenario].md        ← one test plan per end-to-end user journey
test-reports/
  [scenario]-YYYY-MM-DD.md ← generated after each run
```

---

## Running Tests

When asked to run a test plan:

1. Read `test-plans/RULES.md` first
2. Read the target test plan
3. Execute each test case using browser tools (snapshot, click, fill, assert)
4. Generate a report in `test-reports/`

---

## Writing Test Plans

1. Copy `test-plans/TEMPLATE.md`
2. Fill in Meta, Flow, Test Cases, and any module-specific Rules
3. Each test case must have: type, steps, expected result, and assertions

---

## Key Rules

- Never guess — always snapshot the browser before acting
- Never hardcode credentials — use env variables
- On failure: screenshot, note what happened, continue to next test case
- Every assertion must be explicitly checked and marked pass/fail
- Reuse existing test data — don't create new records unless required
