"""
Builds a GitHub Pages site from reporting/metrics/ markdown files.

Usage:
    py reporting/build-site.py

Output: docs/index.html + docs/reports/*.html
"""

import re
import html
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
METRICS_DIR = PROJECT_ROOT / "reporting" / "metrics"
DOCS_DIR = PROJECT_ROOT / "docs"
REPORTS_OUT = DOCS_DIR / "reports"


def md_to_html(md_content: str) -> str:
    """Simple markdown to HTML converter for tables, headers, lists, blockquotes."""
    lines = md_content.split("\n")
    html_lines = []
    in_table = False
    in_list = False
    in_blockquote = False
    table_header_done = False

    for line in lines:
        stripped = line.strip()

        # Skip horizontal rules
        if stripped == "---":
            if in_table:
                html_lines.append("</tbody></table></div>")
                in_table = False
                table_header_done = False
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_blockquote:
                html_lines.append("</blockquote>")
                in_blockquote = False
            html_lines.append("<hr>")
            continue

        # Close list if not a list item
        if in_list and not stripped.startswith("- ") and not stripped.startswith("  -"):
            html_lines.append("</ul>")
            in_list = False

        # Close blockquote
        if in_blockquote and not stripped.startswith(">") and stripped:
            html_lines.append("</blockquote>")
            in_blockquote = False

        # Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]

            # Skip separator row
            if all(re.match(r"^[-:]+$", c) for c in cells):
                table_header_done = True
                continue

            if not in_table:
                html_lines.append('<div class="table-wrap"><table>')
                html_lines.append("<thead><tr>")
                for cell in cells:
                    html_lines.append(f"<th>{inline_format(cell)}</th>")
                html_lines.append("</tr></thead><tbody>")
                in_table = True
                continue

            html_lines.append("<tr>")
            for cell in cells:
                html_lines.append(f"<td>{inline_format(cell)}</td>")
            html_lines.append("</tr>")
            continue

        if in_table:
            html_lines.append("</tbody></table></div>")
            in_table = False
            table_header_done = False

        # Headers
        h_match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if h_match:
            level = len(h_match.group(1))
            text = inline_format(h_match.group(2))
            html_lines.append(f"<h{level}>{text}</h{level}>")
            continue

        # Blockquotes
        if stripped.startswith(">"):
            text = stripped.lstrip("> ").strip()
            if not in_blockquote:
                html_lines.append("<blockquote>")
                in_blockquote = True
            if text:
                html_lines.append(f"<p>{inline_format(text)}</p>")
            continue

        # Lists
        list_match = re.match(r"^(\s*)- (.+)$", stripped)
        if list_match:
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            text = inline_format(list_match.group(2))
            html_lines.append(f"<li>{text}</li>")
            continue

        # Paragraphs
        if stripped:
            html_lines.append(f"<p>{inline_format(stripped)}</p>")
        elif not in_table:
            pass  # blank line

    if in_table:
        html_lines.append("</tbody></table></div>")
    if in_list:
        html_lines.append("</ul>")
    if in_blockquote:
        html_lines.append("</blockquote>")

    return "\n".join(html_lines)


def inline_format(text: str) -> str:
    """Convert inline markdown: bold, italic, code, links, checkboxes."""
    text = html.escape(text)
    # Bold
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Code
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # Checkboxes
    text = text.replace("[x]", "&#9745;")
    text = text.replace("[!]", "&#9746;")
    text = text.replace("[ ]", "&#9744;")
    return text


REPORT_CONFIG = [
    ("completeness-report.md", "Report Completeness", "quality", "Enforces RULES.md standards on every test report"),
    ("cost-report.md", "Cost Report", "cost", "Tracks verification API costs per run"),
    ("duration-report.md", "Duration Tracker", "duration", "Execution time trends and performance alerts"),
    ("failure-heatmap.md", "Failure Heatmap", "failures", "Which TCs and phases fail most often"),
    ("flaky-report.md", "Flaky Tests", "flaky", "Tests that flip between pass and fail"),
    ("drift-history.md", "Drift History", "drift", "Plan edits vs test failure correlation"),
    ("coverage-gaps.md", "Coverage Gaps", "coverage", "Untested features and areas"),
    ("stale-plans.md", "Stale Plans", "stale", "Plans not run recently"),
]


def build_report_page(md_file: Path, title: str, slug: str, description: str) -> str:
    """Build a single report HTML page."""
    content = md_file.read_text(encoding="utf-8")
    body = md_to_html(content)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Test Suite Dashboard</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<nav>
  <a href="../index.html" class="nav-brand">Test Suite Dashboard</a>
  <div class="nav-links">
    {"".join(f'<a href="{s}.html" class="{"active" if s == slug else ""}">{t}</a>' for _, t, s, _ in REPORT_CONFIG)}
  </div>
</nav>
<main>
{body}
</main>
<footer>
  <p>Generated {datetime.now().strftime("%Y-%m-%d %H:%M")} &mdash; <a href="https://github.com/Tshepiso-R/markdown-tests">markdown-tests</a></p>
</footer>
</body>
</html>"""


def build_index() -> str:
    """Build the main dashboard index page."""
    # Read key metrics from reports
    cards_html = ""

    # Completeness
    comp_file = METRICS_DIR / "completeness-report.md"
    if comp_file.exists():
        content = comp_file.read_text(encoding="utf-8")
        avg_match = re.search(r"Average completeness\s*\|\s*([\d.]+)%", content)
        avg = avg_match.group(1) if avg_match else "—"
        cards_html += f"""
        <a href="reports/quality.html" class="card">
          <div class="card-icon">&#9745;</div>
          <div class="card-value">{avg}%</div>
          <div class="card-label">Report Quality</div>
        </a>"""

    # Cost
    cost_file = METRICS_DIR / "cost-report.md"
    if cost_file.exists():
        content = cost_file.read_text(encoding="utf-8")
        total_match = re.search(r"Total Estimated Cost.*?R([\d.]+)", content)
        total = total_match.group(1) if total_match else "—"
        cards_html += f"""
        <a href="reports/cost.html" class="card">
          <div class="card-icon">&#128176;</div>
          <div class="card-value">R{total}</div>
          <div class="card-label">Total API Cost</div>
        </a>"""

    # Duration
    dur_file = METRICS_DIR / "duration-report.md"
    if dur_file.exists():
        content = dur_file.read_text(encoding="utf-8")
        avg_match = re.search(r"Average run duration\s*\|\s*\*\*(\d+)\s*min\*\*", content)
        avg = avg_match.group(1) if avg_match else "—"
        cards_html += f"""
        <a href="reports/duration.html" class="card">
          <div class="card-icon">&#9201;</div>
          <div class="card-value">{avg} min</div>
          <div class="card-label">Avg Run Duration</div>
        </a>"""

    # Flaky
    flaky_file = METRICS_DIR / "flaky-report.md"
    if flaky_file.exists():
        content = flaky_file.read_text(encoding="utf-8")
        flaky_match = re.search(r"Flaky.*?\|\s*\*\*(\d+)\*\*", content)
        count = flaky_match.group(1) if flaky_match else "0"
        cards_html += f"""
        <a href="reports/flaky.html" class="card {"card-green" if count == "0" else "card-red"}">
          <div class="card-icon">&#128260;</div>
          <div class="card-value">{count}</div>
          <div class="card-label">Flaky Tests</div>
        </a>"""

    # Failures
    fail_file = METRICS_DIR / "failure-heatmap.md"
    if fail_file.exists():
        content = fail_file.read_text(encoding="utf-8")
        fail_match = re.search(r"Failed\s*\|\s*\*\*(\d+)\*\*", content)
        count = fail_match.group(1) if fail_match else "0"
        cards_html += f"""
        <a href="reports/failures.html" class="card {"card-green" if count == "0" else "card-red"}">
          <div class="card-icon">&#128293;</div>
          <div class="card-value">{count}</div>
          <div class="card-label">Total Failures</div>
        </a>"""

    # Stale
    stale_file = METRICS_DIR / "stale-plans.md"
    if stale_file.exists():
        content = stale_file.read_text(encoding="utf-8")
        stale_match = re.search(r"Stale.*?\|\s*\*\*(\d+)\*\*", content)
        count = stale_match.group(1) if stale_match else "0"
        cards_html += f"""
        <a href="reports/stale.html" class="card {"card-yellow" if int(count) > 0 else "card-green"}">
          <div class="card-icon">&#128337;</div>
          <div class="card-value">{count}</div>
          <div class="card-label">Stale Plans</div>
        </a>"""

    # Report links
    report_links = ""
    for md_name, title, slug, description in REPORT_CONFIG:
        md_path = METRICS_DIR / md_name
        if md_path.exists():
            report_links += f"""
            <a href="reports/{slug}.html" class="report-link">
              <strong>{title}</strong>
              <span>{description}</span>
            </a>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Test Suite Dashboard</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<nav>
  <a href="index.html" class="nav-brand">Test Suite Dashboard</a>
  <div class="nav-links">
    {"".join(f'<a href="reports/{s}.html">{t}</a>' for _, t, s, _ in REPORT_CONFIG)}
  </div>
</nav>
<main>
  <h1>Test Suite Dashboard</h1>
  <p class="subtitle">Markdown-driven testing &mdash; LandBank CRM QA</p>

  <div class="cards">
    {cards_html}
  </div>

  <h2>Reports</h2>
  <div class="report-grid">
    {report_links}
  </div>
</main>
<footer>
  <p>Generated {datetime.now().strftime("%Y-%m-%d %H:%M")} &mdash; <a href="https://github.com/Tshepiso-R/markdown-tests">markdown-tests</a></p>
</footer>
</body>
</html>"""


CSS = """
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #e6edf3;
  --text-muted: #8b949e;
  --accent: #58a6ff;
  --green: #3fb950;
  --red: #f85149;
  --yellow: #d29922;
  --orange: #db6d28;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

nav {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  overflow-x: auto;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  color: var(--text);
  font-weight: 700;
  font-size: 16px;
  text-decoration: none;
  white-space: nowrap;
}

.nav-links {
  display: flex;
  gap: 4px;
  overflow-x: auto;
}

.nav-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 13px;
  padding: 4px 10px;
  border-radius: 6px;
  white-space: nowrap;
  transition: all 0.15s;
}

.nav-links a:hover { color: var(--text); background: var(--border); }
.nav-links a.active { color: var(--accent); background: rgba(88, 166, 255, 0.1); }

main {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 24px;
}

h1 { font-size: 28px; margin-bottom: 4px; }
h2 { font-size: 20px; margin: 32px 0 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
h3 { font-size: 16px; margin: 24px 0 8px; color: var(--accent); }
h4 { font-size: 14px; margin: 16px 0 8px; }

.subtitle { color: var(--text-muted); margin-bottom: 32px; }

p { margin: 8px 0; }

/* Cards */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  margin: 24px 0;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  text-decoration: none;
  color: var(--text);
  transition: all 0.2s;
}

.card:hover { border-color: var(--accent); transform: translateY(-2px); }
.card-green { border-color: var(--green); }
.card-red { border-color: var(--red); }
.card-yellow { border-color: var(--yellow); }
.card-icon { font-size: 28px; margin-bottom: 8px; }
.card-value { font-size: 32px; font-weight: 700; }
.card-label { font-size: 13px; color: var(--text-muted); margin-top: 4px; }

/* Report grid */
.report-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
}

.report-link {
  display: block;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  text-decoration: none;
  color: var(--text);
  transition: all 0.15s;
}

.report-link:hover { border-color: var(--accent); }
.report-link strong { display: block; margin-bottom: 4px; }
.report-link span { font-size: 13px; color: var(--text-muted); }

/* Tables */
.table-wrap { overflow-x: auto; margin: 16px 0; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th, td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

th {
  background: var(--surface);
  font-weight: 600;
  position: sticky;
  top: 49px;
}

tr:hover td { background: rgba(88, 166, 255, 0.04); }

/* Inline */
code {
  background: var(--surface);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  border: 1px solid var(--border);
}

strong { color: var(--text); }

blockquote {
  border-left: 3px solid var(--accent);
  padding: 8px 16px;
  margin: 16px 0;
  color: var(--text-muted);
  background: rgba(88, 166, 255, 0.04);
  border-radius: 0 8px 8px 0;
}

ul { padding-left: 24px; margin: 8px 0; }
li { margin: 4px 0; }

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 24px 0;
}

footer {
  text-align: center;
  padding: 32px;
  color: var(--text-muted);
  font-size: 13px;
  border-top: 1px solid var(--border);
  margin-top: 48px;
}

footer a { color: var(--accent); text-decoration: none; }
footer a:hover { text-decoration: underline; }

@media (max-width: 768px) {
  .cards { grid-template-columns: repeat(2, 1fr); }
  .report-grid { grid-template-columns: 1fr; }
  nav { flex-direction: column; align-items: flex-start; }
}
"""


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    REPORTS_OUT.mkdir(exist_ok=True)

    # Write CSS
    (DOCS_DIR / "style.css").write_text(CSS, encoding="utf-8")
    print("  style.css")

    # Build individual report pages
    built = 0
    for md_name, title, slug, description in REPORT_CONFIG:
        md_path = METRICS_DIR / md_name
        if md_path.exists():
            page_html = build_report_page(md_path, title, slug, description)
            (REPORTS_OUT / f"{slug}.html").write_text(page_html, encoding="utf-8")
            print(f"  reports/{slug}.html <- {md_name}")
            built += 1
        else:
            print(f"  SKIP {md_name} (not found)")

    # Build index
    index_html = build_index()
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  index.html")

    print(f"\nBuilt {built} report pages + index")
    print(f"Site output: {DOCS_DIR}")
    print(f"\nTo preview locally:")
    print(f"  cd docs && python -m http.server 8080")
    print(f"  Open http://localhost:8080")


if __name__ == "__main__":
    main()
