# Test Execution Rules

These rules govern how Claude should execute markdown test plans.

---

## Before Testing

1. **Read the full test plan** before touching the browser
2. **Check prereqs** — if login is needed, do it first using env credentials
3. **Navigate to the target URL** and take a snapshot to confirm you're on the right page
4. **Do not guess** — if the UI doesn't match the test plan, stop and report the discrepancy

---

## During Testing

### Navigation
- Use browser snapshot before every action to see current state
- Never assume a page has loaded — verify with a snapshot
- If a page redirects unexpectedly, note it and continue

### Filling Forms
- Always snapshot after filling each field to confirm the value took
- For dropdowns: snapshot to see available options, then select
- For date pickers: use keyboard input if the picker is complex
- Clear existing field values before typing new ones

### Clicking / Submitting
- Snapshot before clicking to confirm the target is visible
- Snapshot after clicking to verify the outcome
- If a dialog/modal appears, handle it and note it in the report

### Waiting
- Never use arbitrary delays
- Use `browser_wait_for` with a visible element or URL change
- If something takes more than 30 seconds, mark it as a potential performance issue

---

## Assertions

- For each assertion in the test case, explicitly verify it via snapshot or page content
- Mark each assertion checkbox: `[x]` for pass, `[!]` for fail
- If an assertion fails, capture a screenshot and continue to the next test case
- Never skip assertions — every one must be evaluated

---

## On Failure

1. **Screenshot** the current state
2. **Note** the exact step that failed
3. **Note** what was expected vs what actually happened
4. **Continue** to the next test case (don't abort the whole run)
5. If the failure blocks subsequent tests (e.g., record not created), note which tests were skipped and why

---

## During Each Test Case — Capture Evidence

For each test case section in the report, include:

1. **Page URL** — Record the browser URL at the start of each test case
2. **Snapshots** — Take a screenshot at key moments:
   - After navigating to the target page
   - After filling forms (before save/submit)
   - After save/submit (showing success message or error)
   - Any dialog content (verification tabs, pre-screening, etc.)
3. **Save screenshots** to the report with descriptive names: `tc01-lead-created.png`, `tc06-id-verification.png`, etc.
4. **Embed in report** using: `![Description](../screenshots/filename.png)`

### Report Section Format

Each TC section must include:
```
## TC-XX: Description
**URL:** https://landbankcrm-adminportal-qa.shesha.app/dynamic/...
### Steps Followed
...
### Snapshots
| Screenshot | Description |
|-----------|-------------|
| tc01-lead-form.png | Lead creation form filled |
| tc01-lead-saved.png | Lead saved, visible in table |
### Input vs Output
...
```

---

## After Testing

1. Fill in the **Report Structure** section from the test plan
2. Save the report to `test-reports/[module]-YYYY-MM-DDTHH-MM.md` (include time)
3. Save screenshots to `test-reports/screenshots/[report-name]/` folder
4. Summarize: total pass/fail/skip, top issues, and recommendations
5. If any test plan steps are outdated (UI changed), note what needs updating

---

## Step Execution — Zero Tolerance for Skipping

> **CRITICAL:** This rule exists because a prior run (2026-03-17) falsely passed TC-06 by skipping 5 verification steps.

- **Execute EVERY step** in the test case, in order, one at a time
- **Never jump ahead** to a final action (Save, Submit, Finalise) before completing all preceding steps
- **If a step says "click"** — click it and snapshot the result
- **If a step says "review"** — open the content, snapshot it, and document what was seen
- **If a dialog has multiple tabs** — click EACH tab and snapshot EACH one before closing
- **If you are about to skip a step** — STOP. Go back and execute it.
- A test case with skipped steps is a **FAIL**, not a PASS
- **NEVER use a different record** to complete a test case — if YOUR test data can't reach a step, mark it FAIL and explain why
- **NEVER work around** a discrepancy by substituting data — report it as a failure

---

## Verification Review — Must Review Every Individual

> Before clicking "Finalise Verification Outcomes", ALL individuals must be reviewed.

**Personal loan:** Verify Main Applicant + Spouse (if married)
**Entity loan:** Verify ALL — Entity (CIPC) + ALL Directors + ALL Signatories

For EACH individual listed in verifications:
1. Click their "Awaiting Review" button
2. **ID Verification tab** — assert:
   - Name Match: Passed/Failed/Requires Review
   - ID Match: Passed/Failed
   - Death Check: Passed/Failed
   - Outcome: Passed/Failed/TBD
   - **Always** select a Review Decision (Approve if all passed, Reject if failed)
   - Click Submit on the review
3. **KYC Verification tab** — assert:
   - First Name Match Status: Passed/Failed
   - Outcome: Passed/Failed
   - **Always** select KYC First Name Review Decision (Approve if passed)
4. Close dialog
5. Repeat for EVERY individual

**Before clicking Finalise:**
- Verify ZERO "Awaiting Review" buttons remain
- Only then click "Finalise Verification Outcomes"

**Report format per individual** (no tables — use assertion lists):
```
### Individual: [Name] ([ID Number])
**ID Verification:** Status: [X] | Date: [X]
- Submitted: [First Name] [Last Name], [ID Number]
- Returned: [FIRST NAME] [LAST NAME], [ID Number], DOB [X], [Gender]
- [x] Name Match: Passed
- [x] ID Match: Passed
- [x] Death Check: Passed
- [x] Outcome: Passed
- Review Decision: Approve (selected + submitted)
**KYC Verification:** Status: [X] | Date: [X]
- Submitted: [ID Number]
- Returned: [First Name], Address: [X], Cell: [X], Employer: [X]
- [x] First Name Match: Passed
- [x] Outcome: Passed
- KYC First Name Review Decision: Approve (selected)
```

---

## Test Data — Reuse IDs (Cost Rule)

> **CRITICAL:** Each new SA ID number triggers a paid verification API call. Always reuse the approved IDs below.

| Person | ID Number | Use For |
|--------|-----------|---------|
| Ian Houvet | 7708206169188 | Personal loan applicant, Entity director (Married) |
| Chamaine Houvet | 7304190225085 | Entity director (Single), Spouse of Ian |
| Xolile Ndlangana | 6311115651080 | Entity director (Single) |

**Entity registration:** 2012/225386/07 (Boxfusion)

**Email address:** Use testmail.app — `5s9ku.consent-[unique]@inbox.testmail.app`
- Do NOT use `promise.raganya@boxfusion.io` — that inbox can't be queried programmatically
- The tag (e.g. `consent-1710850000000`) must be unique per run for email isolation

- **NEVER** generate or randomize ID numbers
- **NEVER** use a new ID number not in this list
- **ALWAYS** use testmail.app email addresses for leads (required for consent flow)
- The **unique part** of each test run is the lead First Name (e.g. AutoCI12345) — not the ID
- If a test requires a different person, ask the user for an approved ID first

---

## Consent Flow — Testmail.app API

> **Every loan application requires consent.** Auto Verify is for internal testing only — the real flow includes email consent + OTP.

| Field | Value |
|-------|-------|
| Service | testmail.app |
| Namespace | 5s9ku |
| API Key | b300bfdf-3e55-4478-9e27-072849073ed4 |
| Email format | `5s9ku.{tag}@inbox.testmail.app` |

**API call to retrieve emails:**
```
GET https://api.testmail.app/api/json?apikey=b300bfdf-3e55-4478-9e27-072849073ed4&namespace=5s9ku&tag={tag}&livequery=true&timeout=60000
```

**Consent flow steps:**
1. Uncheck Auto Verify on opportunity before initiating
2. After Initiate → status becomes "Consent Pending"
3. Retrieve consent email (Subject: "Action Required: Provide Consent", from notifications@smartgov.co.za)
4. Extract consent URL (href matching `individual-application-consent`)
5. Open consent page → Click "Request OTP"
6. Retrieve OTP email (Subject: "One-Time-Pin")
7. Extract OTP: `Your One-Time-Pin is (\d+)`
8. Submit OTP → Click "Submit OTP and Sign Consent" → Confirm
9. Success: "Thank you for providing consent"
10. Status changes to "Verification In Progress"

---

## What NOT to Do

- Do NOT hardcode credentials in reports or test plans
- Do NOT create new records unless the test explicitly requires it
- Do NOT modify the test plan during execution — report discrepancies instead
- Do NOT skip a test case without documenting why
- Do NOT skip steps within a test case — execute every step sequentially
- Do NOT use new SA ID numbers — reuse the approved list above (verification costs money)
- Do NOT assume a previous test's state carries over — each case is independent
