# Opportunity Entity Edit — Test Report

**Date:** 2026-03-17
**Tester:** System Administrator (admin)
**Environment:** QA (landbankcrm-adminportal-qa.shesha.app)
**Opportunity:** Autommu0nweg Houvet (ID: 6198ff20-f7e7-48ea-9b38-2c950d2860e9)
**Director:** Ian Houvet (SA ID: 7708206169188)

---

## Run Summary
| Field          | Value       |
|---------------|-------------|
| Date          | 2026-03-17  |
| Total cases   | 2           |
| Passed        | 2           |
| Failed        | 0           |
| Skipped       | 0           |
| Duration      | ~10m        |

---

## Results

### TC-11: Complete Entity Client Info — all fields except Marital Regime
- **Result:** Pass
- **Notes:** All Entity Information fields were filled successfully. "Data saved successfully!" message confirmed. Marital Regime in Director table intentionally left empty per test requirements.
- **Fields filled:**

| Field | Value Set | Status |
|-------|-----------|--------|
| Opportunity Owner | Fatima Abrahams | PASS |
| Entity Name | Boxfusion (pre-filled) | PASS |
| Company Registration Number | 2020/123456/23 | PASS |
| Years In Operation | 5 | PASS |
| Contact Person Title | Mr (pre-filled) | PASS |
| Contact Person Name | Ian (changed from Autommu0nweg) | PASS |
| Contact Person Surname | Houvet (pre-filled) | PASS |
| Contact Person Email Address | tinaye.mushore@boxfusion.io (pre-filled) | PASS |
| Contact Person Mobile Number | 0712345678 (pre-filled) | PASS |
| Preferred Communication | Email (pre-filled) | PASS |
| Country Of Residence | South Africa | PASS |
| Citizenship | South Africa | PASS |
| Entity Org Type | Closed Corporation (CC) | PASS |
| Client Classification | Development | PASS |
| BEEE Level | Level 1 | PASS |
| Registered Address | 100 Main Street, Main Street, Marshalltown, Johannesburg, South Africa | PASS |
| Province | Gauteng (pre-filled) | PASS |
| Region | Central Region (auto-mapped) | PASS |
| Provincial Office | Provincial Office | PASS |

### TC-12: Verify Director details with Marital Status but no Marital Regime
- **Result:** Pass
- **Notes:** Director IAN HOUVET confirmed with ID 7708206169188, Marital Status: Single, Marital Regime: empty. Save succeeded without Marital Regime.

| Director Field | Value | Status |
|---------------|-------|--------|
| First Name | Ian | PASS |
| Last Name | Houvet | PASS |
| ID Number | 7708206169188 | PASS |
| Email | tinaye.mushore@boxfusion.io | PASS |
| Mobile | 0712345678 | PASS |
| Marital Status | Single | PASS |
| Marital Regime | (empty — intentional) | PASS |

---

## New Dropdown Values Discovered

### Entity Org Type (new)
| Value |
|-------|
| Pty Ltd |
| Closed Corporation (CC) |
| Trust |

### BEEE Level (new)
| Value |
|-------|
| Level 1 |
| Level 2 |
| Level 3 |
| Level 4 |
| Level 5 |
| Level 6 |
| Level 7 |
| Level 8 |

### Application Status (updated — new value observed)
| Value |
|-------|
| Draft |
| Complete |
| Verification In Progress |

---

## Entity vs Individual — Structural Differences Observed

| Feature | Individual | Entity |
|---------|-----------|--------|
| Client Info section title | "Client Info" | "Entity Information" |
| Name fields | Client Name, Client Surname | Entity Name, Contact Person Name/Surname |
| ID field | Client ID Number (SA ID) | Company Registration Number |
| Additional fields | — | Years In Operation, Entity Org Type, BEEE Level, Does client have resolution? |
| Directors section | Not present | Present — table with Marital Status, Marital Regime, Spouse details |
| Signatories section | Not present | Present — table with Name, ID, Email, Mobile |
| Marital fields | Marital Status on main form | Marital Status + Marital Regime per director |

---

## Issues Found
| # | Test Case | Severity | Description |
|---|-----------|----------|-------------|
| 1 | TC-11 | Low | **Director search link has empty ID** — clicking the search icon on a director row navigates to `/dynamic/LandBank.Crm/LBApplication-director-details?id=` with no ID value |
| 2 | TC-11 | Info | **Empty director row** — first row in Directors table is completely empty (no data). May be a ghost record. |
| 3 | TC-11 | Info | **Console errors persist** — `executeScriptSync error TypeError` errors throughout the session (same as previous exploration) |

---

## Recommendations
1. **Test "Initiate Loan Application" with missing Marital Regime** — verify whether the empty Marital Regime blocks the loan application workflow
2. **Fix director detail link** — the search icon on director rows links to a URL with empty ID parameter
3. **Clean up empty director row** — investigate the blank first row in the Directors table
4. **Test adding a new director** — verify the "Add Director" flow and whether Marital Regime is required there
5. **Test Entity with resolution** — check behavior when "Does the client have a resolution?" checkbox is ticked
