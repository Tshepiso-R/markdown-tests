# Azure DevOps Pipeline Setup

## Prerequisites

1. Azure DevOps project with this repo connected
2. Anthropic API key with Claude access
3. QA environment credentials

## Pipeline Variables (Secrets)

Add these as **secret variables** in the pipeline settings (Pipelines > Edit > Variables):

| Variable | Description | Example |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude Code | `sk-ant-...` |
| `ADMIN_PASSWORD` | Admin account password for QA environment | `****` |
| `RM_PASSWORD` | Fatima Abrahams account password | `****` |

**Mark all three as secrets** (lock icon) so they are not exposed in logs.

## How It Runs

1. **Triggers:** On push to `test-plans/**` on main, or weekday mornings at 06:00 UTC
2. **Manual runs:** Go to Pipelines > Run pipeline > Select test plan from dropdown
3. **What happens:**
   - Installs Claude Code CLI, Playwright, and MCP Playwright server
   - Claude reads the test plan and drives a headless Chromium browser
   - Executes all test cases (TC-01 through TC-08)
   - Generates a markdown report in `test-reports/`
   - Publishes report as a pipeline artifact
   - Commits report back to the repo (on main branch runs)

## Pipeline Artifacts

After each run, download artifacts from the pipeline run summary:
- `test-results/test-reports/` — Markdown test report
- `test-results/claude-output.log` — Full Claude execution log

## Timeout

The pipeline has a 30-minute timeout for the test execution step. A full run typically takes 10-15 minutes.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "ANTHROPIC_API_KEY not set" | Add the secret variable in pipeline settings |
| Browser launch fails | The pipeline uses `--headless` mode; ensure `npx playwright install` succeeded |
| Test fails at login | Check that QA environment is up and credentials are correct |
| Timeout exceeded | Increase `timeoutInMinutes` in the YAML or check if QA is slow |
| Report not committed | Ensure pipeline has "Contribute" permission on the repo (Project Settings > Repos > Security) |
