# Reporting Suite Setup

All tools read your markdown test reports and generate analysis in `reporting/metrics/`.

---

## Quick Start — Run All Reports

```bash
py reporting/collect-metrics.py
py reporting/convert-to-allure.py --all
py reporting/flaky-monitor.py
py reporting/duration-tracker.py
py reporting/failure-heatmap.py
py reporting/drift-history.py
py reporting/coverage-gaps.py
py reporting/report-completeness.py
py reporting/stale-plans.py
py reporting/cost-report.py
```

---

## Tools

### Allure Reports (Rich HTML)

Converts markdown reports into interactive HTML dashboards with drill-down per TC.

```bash
py reporting/convert-to-allure.py --all
allure generate reporting/allure-results -o reporting/allure-report --clean
allure open reporting/allure-report
```

Install Allure: `npm install -g allure-commandline`

### Metrics Collector (Grafana Data Source)

Extracts pass/fail/skip counts into JSON for Grafana dashboards.

```bash
py reporting/collect-metrics.py
```

Output: `reporting/metrics/test-metrics.json`

### Flaky Test Monitor

Detects tests that flip between PASS and FAIL across runs.

```bash
py reporting/flaky-monitor.py
py reporting/flaky-monitor.py --module personal-loan
```

Output: `reporting/metrics/flaky-report.md`

### Duration Tracker

Tracks execution time per run and per TC. Flags slow runs (>3 min/TC).

```bash
py reporting/duration-tracker.py
```

Output: `reporting/metrics/duration-report.md`

### Failure Heatmap

Shows which TCs and phases fail most often. Lists all flagged issues.

```bash
py reporting/failure-heatmap.py
```

Output: `reporting/metrics/failure-heatmap.md`

### Drift History Log

Correlates git history of test plan edits with test run failures.

```bash
py reporting/drift-history.py
```

Output: `reporting/metrics/drift-history.md`

### Coverage Gap Detector

Compares test plans against app features. Finds untested areas.

```bash
py reporting/coverage-gaps.py
```

Output: `reporting/metrics/coverage-gaps.md`

### Report Completeness Checker

Enforces RULES.md quality standards: required sections, assertions, screenshots, toast checks.

```bash
py reporting/report-completeness.py
py reporting/report-completeness.py test-reports/personal-loan/personal-loan-2026-03-19T15-18.md
```

Output: `reporting/metrics/completeness-report.md`

### Stale Test Plan Detector

Flags test plans not run within a threshold (default: 7 days).

```bash
py reporting/stale-plans.py
py reporting/stale-plans.py --threshold 14
```

Output: `reporting/metrics/stale-plans.md`

### Cost Report

Tracks verification API costs: ID verifications, KYC lookups, OTP SMS, per run and cumulative.

```bash
py reporting/cost-report.py
```

Output: `reporting/metrics/cost-report.md`

Update pricing in `COSTS` dict inside `cost-report.py` to match your vendor rates.

---

## Grafana Dashboard (Optional)

1. Start Grafana: `docker run -d -p 3000:3000 grafana/grafana-oss`
2. Install Infinity plugin: `grafana-cli plugins install yesoreyeram-infinity-datasource`
3. Point data source to: `reporting/metrics/test-metrics.json`
4. Import: `reporting/grafana/dashboard.json`

---

## File Structure

```
reporting/
  SETUP.md                 ← this file
  convert-to-allure.py     ← markdown → Allure JSON
  collect-metrics.py        ← markdown → metrics JSON
  flaky-monitor.py          ← flaky test detection
  duration-tracker.py       ← execution time trends
  failure-heatmap.py        ← failure frequency analysis
  drift-history.py          ← plan edit vs failure correlation
  coverage-gaps.py          ← untested feature detection
  report-completeness.py    ← report quality enforcement
  stale-plans.py            ← stale plan detection
  cost-report.py            ← verification API cost tracking
  allure-results/           ← generated Allure JSON
  allure-report/            ← generated Allure HTML
  metrics/
    test-metrics.json       ← Grafana data source
    flaky-report.md         ← flaky test report
    duration-report.md      ← duration analysis
    failure-heatmap.md      ← failure heatmap
    drift-history.md        ← drift correlation
    coverage-gaps.md        ← coverage gaps
    completeness-report.md  ← report quality scores
    stale-plans.md          ← stale plan alerts
    cost-report.md          ← cost analysis
  grafana/
    dashboard.json          ← importable Grafana dashboard
```
