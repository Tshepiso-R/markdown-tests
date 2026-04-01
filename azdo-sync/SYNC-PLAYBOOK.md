# Azure DevOps Sync Playbook

> Claude reads this file when asked to sync a markdown test plan to Azure DevOps Test Plans.
> This is NOT a script — Claude follows these instructions and executes API calls via curl.

---

## Configuration

| Field | Value |
|-------|-------|
| Organization | `boxfusion` |
| Project | `markdown-test` |
| API Version | `7.0` |
| PAT env variable | `AZDO_PAT` |
| Mapping file | `azdo-sync/mapping.json` |

> **For other projects:** Replace the org and project above with your own. Store your PAT as a GitHub Secret or environment variable named `AZDO_PAT`. Create a PAT in Azure DevOps with **Test Management (Read & Write)** and **Work Items (Read & Write)** scopes.

### Auth Header

All API calls use Basic auth with the PAT:

```
-u ":$AZDO_PAT"
```

Or as a header:

```
Authorization: Basic $(echo -n ":$AZDO_PAT" | base64)
```

---

## Step 1: Read the Mapping File

Read `azdo-sync/mapping.json` to check if this test plan has already been synced.

- If the plan has an `azdoPlanId` that is NOT null → this is a **re-sync** (update existing items)
- If the plan has `azdoPlanId: null` → this is a **first sync** (create everything)

---

## Step 2: Parse the Markdown Test Plan

Read the target test plan (e.g., `test-plans/e2e-personal-loan-application.md`) and extract:

| Markdown Element | What to Extract |
|-----------------|-----------------|
| `# Test Plan: [Name]` | Test Plan name |
| `## Meta` table | Description (Module field) |
| `## PHASE N: [Name]` | Test Suite name (one per phase) |
| `### TC-XX: [Description]` | Test Case title |
| `- **Type:**` | Priority mapping: Happy path → 2, Negative → 3, Edge case → 3 |
| `- **Steps:**` numbered list | Action steps |
| `- **Expected result:**` | Overall expected outcome (goes in Description) |
| `- **Assertions:**` checkbox list | Validation steps |
| `- **Input data:**` table | Shared parameters (goes in Description) |

### Handling Sub-Cases

Test cases like `TC-05a`, `TC-05b`, `TC-05c` are sub-cases. They belong to the **same phase/suite** as their parent `TC-05`. Treat each as a separate Test Case work item.

---

## Step 3: Create or Update the Test Plan

### First Sync — Create Test Plan

```bash
curl -s -u ":$AZDO_PAT" \
  -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/boxfusion/markdown-test/_apis/testplan/plans?api-version=7.0" \
  -d '{
    "name": "[Plan Name from H1]",
    "description": "[Module field from Meta table]",
    "state": "Active"
  }'
```

Save the returned `id` as `azdoPlanId` in mapping.json.

> **Note:** Every new Test Plan comes with a default root suite. Get it:

```bash
curl -s -u ":$AZDO_PAT" \
  "https://dev.azure.com/boxfusion/markdown-test/_apis/testplan/plans/{planId}/suites?api-version=7.0"
```

The root suite ID is needed as `parentSuiteId` when creating phase suites.

### Re-Sync — Update Test Plan

```bash
curl -s -u ":$AZDO_PAT" \
  -X PATCH \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/boxfusion/markdown-test/_apis/testplan/plans/{planId}?api-version=7.0" \
  -d '{
    "name": "[Updated Plan Name]",
    "description": "[Updated description]"
  }'
```

---

## Step 4: Create or Update Test Suites (one per PHASE)

### Create Suite

```bash
curl -s -u ":$AZDO_PAT" \
  -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/boxfusion/markdown-test/_apis/testplan/plans/{planId}/suites?api-version=7.0" \
  -d '{
    "suiteType": "staticTestSuite",
    "name": "PHASE 1: Lead Capture",
    "parentSuite": {
      "id": {rootSuiteId}
    }
  }'
```

Save the returned `id` as `azdoSuiteId` in mapping.json for this phase.

### Update Suite (re-sync)

If the suite already exists (has an ID in mapping.json), update its name if changed:

```bash
curl -s -u ":$AZDO_PAT" \
  -X PATCH \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/boxfusion/markdown-test/_apis/testplan/plans/{planId}/suites/{suiteId}?api-version=7.0" \
  -d '{
    "name": "PHASE 1: Lead Capture (Updated)"
  }'
```

---

## Step 5: Create or Update Test Cases

### Convert Steps + Assertions to XML

Each test case's steps and assertions become an XML string for the `Microsoft.VSTS.TCM.Steps` field.

**Rules:**
- Numbered steps → `type="ActionStep"` — first `parameterizedString` = action, second = **what should happen** (dialog opens, form loads, toast appears, page redirects, etc.). NEVER leave the expected result empty.
- Assertions → `type="ValidateStep"` — first `parameterizedString` = what to check, second = **the expected result** (NOT "Pass" — describe what should happen)
- Step IDs are sequential starting at 1
- The `last` attribute on `<steps>` = total number of steps

**Example — TC-01:**

Markdown:
```
- **Steps:**
  1. Navigate to Leads via sidebar menu
  2. Click "New Lead"
  3. Fill all required fields (see input data)
  4. Click OK
- **Assertions:**
  - [ ] Lead appears at top of Leads table
  - [ ] Lead status: "New"
  - [ ] All fields saved correctly
```

XML:
```xml
<steps id="0" last="7">
  <step id="1" type="ActionStep">
    <parameterizedString isformatted="true">Navigate to Leads via sidebar menu</parameterizedString>
    <parameterizedString isformatted="true"></parameterizedString>
  </step>
  <step id="2" type="ActionStep">
    <parameterizedString isformatted="true">Click "New Lead"</parameterizedString>
    <parameterizedString isformatted="true"></parameterizedString>
  </step>
  <step id="3" type="ActionStep">
    <parameterizedString isformatted="true">Fill all required fields (see input data)</parameterizedString>
    <parameterizedString isformatted="true"></parameterizedString>
  </step>
  <step id="4" type="ActionStep">
    <parameterizedString isformatted="true">Click OK</parameterizedString>
    <parameterizedString isformatted="true"></parameterizedString>
  </step>
  <step id="5" type="ValidateStep">
    <parameterizedString isformatted="true">Check Leads table</parameterizedString>
    <parameterizedString isformatted="true">Lead appears at top of Leads table</parameterizedString>
  </step>
  <step id="6" type="ValidateStep">
    <parameterizedString isformatted="true">Check lead status badge</parameterizedString>
    <parameterizedString isformatted="true">Lead status shows "New"</parameterizedString>
  </step>
  <step id="7" type="ValidateStep">
    <parameterizedString isformatted="true">Verify all saved fields</parameterizedString>
    <parameterizedString isformatted="true">All fields match entered values</parameterizedString>
  </step>
</steps>
```

### Create Test Case Work Item

```bash
curl -s -u ":$AZDO_PAT" \
  -X POST \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/boxfusion/markdown-test/_apis/wit/workitems/\$Test%20Case?api-version=7.0" \
  -d '[
    {
      "op": "add",
      "path": "/fields/System.Title",
      "value": "TC-01: Create Individual lead"
    },
    {
      "op": "add",
      "path": "/fields/System.Description",
      "value": "<p><b>Type:</b> Happy path<br><b>Login:</b> admin<br><b>Expected:</b> Lead created with status New</p>"
    },
    {
      "op": "add",
      "path": "/fields/Microsoft.VSTS.TCM.Steps",
      "value": "<steps id=\"0\" last=\"7\">...</steps>"
    },
    {
      "op": "add",
      "path": "/fields/Microsoft.VSTS.Common.Priority",
      "value": 2
    }
  ]'
```

Save the returned `id` as `azdoWorkItemId` in mapping.json.

### Update Test Case (re-sync)

```bash
curl -s -u ":$AZDO_PAT" \
  -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/boxfusion/markdown-test/_apis/wit/workitems/{workItemId}?api-version=7.0" \
  -d '[
    {
      "op": "replace",
      "path": "/fields/System.Title",
      "value": "TC-01: Create Individual lead (updated)"
    },
    {
      "op": "replace",
      "path": "/fields/Microsoft.VSTS.TCM.Steps",
      "value": "<steps>...</steps>"
    }
  ]'
```

> **Error handling:** If a PATCH returns 404 (work item deleted in AzDO), create a new work item and update mapping.json with the new ID.

---

## Step 6: Add Test Cases to Suites

After creating a test case work item, add it to its phase's suite:

```bash
curl -s -u ":$AZDO_PAT" \
  -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/boxfusion/markdown-test/_apis/testplan/plans/{planId}/suites/{suiteId}/testcase?api-version=7.0" \
  -d '[
    {
      "workItem": { "id": {workItemId} }
    }
  ]'
```

---

## Step 7: Update Mapping File

After all API calls complete, update `azdo-sync/mapping.json` with:
- All AzDO IDs (plan, suites, test cases)
- `lastSyncDate`: current ISO timestamp
- `lastSyncHash`: a short identifier (e.g., first 8 chars of the test plan file's git hash, or a content-based hash)

---

## Step 8: Report Results

Print a summary:

```
Synced: [Plan Name]
  - Test Plan ID: {azdoPlanId}
  - Suites created/updated: N
  - Test Cases created/updated: N
  - AzDO URL: https://dev.azure.com/boxfusion/markdown-test/_testPlans/execute?planId={planId}
```

---

## Rate Limiting

Azure DevOps has API rate limits. If creating many items:
- Pause 500ms between work item creation calls
- If you get a 429 response, wait 5 seconds and retry

---

## Checklist Before Sync

- [ ] `AZDO_PAT` environment variable is set
- [ ] PAT has Test Management + Work Items read/write scope
- [ ] Target test plan markdown file exists and is valid
- [ ] `azdo-sync/mapping.json` exists (even if all IDs are null)
