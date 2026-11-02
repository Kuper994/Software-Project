#!/usr/bin/env python3
"""Add the 2026-2027 course pages to the existing Sphinx-built website.

Run this script from the root of the Software-Project repository, on the
course-2026-2027 branch. It keeps the existing theme, lecture pages, and assets.
"""

from pathlib import Path
import re
import shutil
import sys
from html import escape

ROOT = Path.cwd()
INTRO = ROOT / "intro.html"

if not INTRO.is_file():
    sys.exit("Error: run this script from the repository root (intro.html was not found).")

source = INTRO.read_text(encoding="utf-8")

# Keep the existing navigation and append links to the new course pages.
nav_pattern = re.compile(
    r'(<nav class="bd-links bd-docs-nav".*?</nav>)',
    flags=re.DOTALL
)
nav_match = nav_pattern.search(source)
if not nav_match:
    sys.exit("Error: could not find the existing Sphinx sidebar navigation in intro.html.")

nav = nav_match.group(1)
new_links = (
    '<li class="toctree-l1"><a class="reference internal" href="schedule.html">'
    'Course Schedule</a></li>\n'
    '<li class="toctree-l1"><a class="reference internal" href="administration.html">'
    'Course Administration</a></li>\n'
)
# Insert links into the first navigation list, without changing existing entries.
list_end = nav.find("</ul>")
if list_end < 0:
    sys.exit("Error: could not find the navigation list in intro.html.")
nav = nav[:list_end] + new_links + nav[list_end:]

def make_page(page_name, title, article, toc_items):
    """Create a new page using the existing Introduction page as its template."""
    page = source
    page = re.sub(
        r"<title>.*?</title>",
        f"<title>{escape(title)} &#8212; Software Project&lt;br&gt;0368-2161</title>",
        page,
        count=1,
        flags=re.DOTALL
    )
    page = page.replace(
        "DOCUMENTATION_OPTIONS.pagename = 'intro';",
        f"DOCUMENTATION_OPTIONS.pagename = '{page_name}';"
    )
    page = re.sub(
        r'<article class="bd-article">.*?</article>',
        f'<article class="bd-article">\n{article}\n</article>',
        page,
        count=1,
        flags=re.DOTALL
    )
    page = re.sub(
        r'<ul class="visible nav section-nav flex-column">.*?</ul>',
        '<ul class="visible nav section-nav flex-column">\n'
        + toc_items + '\n</ul>',
        page,
        count=1,
        flags=re.DOTALL
    )
    page = nav_pattern.sub(nav, page, count=1)
    # These standalone pages do not have a meaningful previous/next sequence.
    page = re.sub(
        r'<footer class="prev-next-footer d-print-none">.*?</footer>',
        '<footer class="prev-next-footer d-print-none"></footer>',
        page,
        count=1,
        flags=re.DOTALL
    )
    return page

intro_article = r"""
<section class="tex2jax_ignore mathjax_ignore" id="introduction">
<h1>Software Project — 2026/2027<a class="headerlink" href="#introduction"
title="Link to this heading">#</a></h1>
<section id="overview">
<h2>Overview<a class="headerlink" href="#overview" title="Link to this heading">#</a></h2>
<p>Welcome to the Software Project course (0368-2161).</p>
<p>The course focuses on large-scale programming, efficient computation, and
real-world applications. Students will develop core programming skills in C
and interface C code with Python pipelines that use data-science libraries.</p>
<p><strong>Course communication:</strong> Moodle forums. Announcements and updates
published in the Moodle course forum are official and binding.</p>
<p><strong>Official course environment:</strong> Linux (Ubuntu).</p>
</section>
<section id="course-objectives">
<h2>Course Objectives<a class="headerlink" href="#course-objectives"
title="Link to this heading">#</a></h2>
<ul>
<li>Large-scale programming</li>
<li>Efficient computation</li>
<li>Real-world applications</li>
<li>Core programming in C, interfaced with Python and data-science libraries</li>
</ul>
</section>
<section id="project">
<h2>Final Project<a class="headerlink" href="#project" title="Link to this heading">#</a></h2>
<p>The course includes a final project. The project submission deadline will be
announced on Moodle.</p>
</section>
<section id="books">
<h2>Recommended Books<a class="headerlink" href="#books" title="Link to this heading">#</a></h2>
<ul>
<li><strong>A Book on C</strong>, 4th edition, by Al Kelley and Ira Pohl,
Addison-Wesley.</li>
<li><strong>Python Data Science Handbook</strong>, by Jake VanderPlas, O'Reilly.</li>
</ul>
</section>
</section>
"""
intro_toc = """
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#overview">Overview</a></li>
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#course-objectives">Course Objectives</a></li>
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#project">Final Project</a></li>
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#books">Recommended Books</a></li>
"""

schedule_rows = [
    ("20.10.2026", "1", "Development Environment + Docker (Yael)", "", "V"),
    ("27.10.2026", "—", "No class", "", "Election Day"),
    ("03.11.2026", "2", "Project (Didi ?)", "", ""),
    ("10.11.2026", "3", "C basics (Didi)", "HW0", ""),
    ("17.11.2026", "4", "C basics (Didi)", "", ""),
    ("24.11.2026", "5", "C basics (Didi)", "HW1", ""),
    ("01.12.2026", "6", "C basics (Didi)", "", ""),
    ("08.12.2026", "7", "C basics (Didi)", "", ""),
    ("15.12.2026", "8", "C-Python + Python Data Science Libraries (Yael)", "", ""),
    ("22.12.2026", "9", "Python Data Science Libraries (Yael)", "HW2", ""),
    ("29.12.2026", "10", "Large-Scale Computing (Yael)", "", "V"),
    ("05.01.2027", "11", "Databases — SQL / NoSQL / PostgreSQL [Change reqs.] (Yael)", "", ""),
    ("12.01.2027", "12", "Parallel / Distributed Computing — CUDA, Docker Compose, etc. (Yael)", "", ""),
    ("18.01.2027", "13", "C Tutorial (?)", "", ""),
]
table_body = []
for i, (date, week, subject, hw, extra) in enumerate(schedule_rows):
    row_class = "row-even" if i % 2 == 0 else "row-odd"
    table_body.append(
        f'<tr class="{row_class}"><td><p>{escape(date)}</p></td>'
        f'<td><p>{escape(week)}</p></td><td><p>{escape(subject)}</p></td>'
        f'<td><p>{escape(hw) if hw else "—"}</p></td>'
        f'<td><p>{escape(extra) if extra else "—"}</p></td></tr>'
    )

schedule_article = r"""
<section class="tex2jax_ignore mathjax_ignore" id="course-schedule">
<h1>Course Schedule — 2026/2027<a class="headerlink" href="#course-schedule"
title="Link to this heading">#</a></h1>
<p>The schedule below is subject to updates. Please follow announcements on Moodle.</p>
<div class="pst-scrollable-table-container">
<table class="table">
<thead><tr class="row-odd">
<th class="head"><p>Date</p></th><th class="head"><p>Week</p></th>
<th class="head"><p>Subject</p></th><th class="head"><p>Homework</p></th>
<th class="head"><p>Notes</p></th></tr></thead>
<tbody>
""" + "\n".join(table_body) + r"""
</tbody></table></div>
<p><strong>Note:</strong> Entries marked with a question mark or bracketed notes
are retained as provided in the course schedule and may need confirmation.</p>
</section>
"""
schedule_toc = """
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#course-schedule">Course Schedule</a></li>
"""

admin_article = r"""
<section class="tex2jax_ignore mathjax_ignore" id="course-administration">
<h1>Course Administration<a class="headerlink" href="#course-administration"
title="Link to this heading">#</a></h1>
<section id="grading">
<h2>Grading<a class="headerlink" href="#grading" title="Link to this heading">#</a></h2>
<p><strong>Final grade:</strong> 50% final project and 50% test.</p>
<p>There are also three additional homework assignments. These are not mandatory.</p>
</section>
<section id="homework-guidelines">
<h2>Homework Guidelines<a class="headerlink" href="#homework-guidelines"
title="Link to this heading">#</a></h2>
<ul>
<li>Follow the instructions provided in each assignment.</li>
<li>Updates published in the Moodle forum are official and binding.</li>
<li>Extensions are granted only in special circumstances.</li>
<li>Students may use AI tools, but are responsible for understanding their code
and testing it according to the assignment instructions.</li>
</ul>
</section>
<section id="appeals">
<h2>Appeals<a class="headerlink" href="#appeals" title="Link to this heading">#</a></h2>
<ul>
<li>Appeals must be submitted within 5 days through the private Moodle forum.</li>
<li>One appeal is allowed per homework assignment.</li>
<li>Only ZIP-file or file-name corrections are permitted; code changes are not.</li>
<li>Corrections may incur a penalty of 5–10 points.</li>
</ul>
</section>
<section id="office-hours">
<h2>Office Hours and Communication<a class="headerlink" href="#office-hours"
title="Link to this heading">#</a></h2>
<p>Office-hour and reception-hour links are available on Moodle. Course
communication takes place through the Moodle forums.</p>
</section>
<section id="military-service">
<h2>Military Service Adjustments<a class="headerlink" href="#military-service"
title="Link to this heading">#</a></h2>
<p><strong>Group C:</strong> Students may submit the final project individually
instead of taking the final exam. They must notify the course staff through
the personal query forum at least 24 hours before the final exam.</p>
<p><strong>Moed C:</strong> Exams are conducted according to university guidelines
for all reserve-service groups.</p>
</section>
</section>
"""
admin_toc = """
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#grading">Grading</a></li>
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#homework-guidelines">Homework Guidelines</a></li>
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#appeals">Appeals</a></li>
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#office-hours">Office Hours and Communication</a></li>
<li class="toc-h2 nav-item toc-entry"><a class="reference internal nav-link"
href="#military-service">Military Service Adjustments</a></li>
"""

# Back up the original landing page before replacing its contents.
backup = ROOT / "intro.html.before-2026-2027"
if not backup.exists():
    shutil.copy2(INTRO, backup)

# Replace the landing page's article and local contents list.
updated_intro = make_page("intro", "Introduction", intro_article, intro_toc)
INTRO.write_text(updated_intro, encoding="utf-8")

(ROOT / "schedule.html").write_text(
    make_page("schedule", "Course Schedule", schedule_article, schedule_toc),
    encoding="utf-8"
)
(ROOT / "administration.html").write_text(
    make_page("administration", "Course Administration", admin_article, admin_toc),
    encoding="utf-8"
)

# Update the sidebar on every existing HTML page so the new pages are reachable.
for html_file in ROOT.glob("*.html"):
    if html_file.name in {"intro.html", "schedule.html", "administration.html"}:
        continue
    text = html_file.read_text(encoding="utf-8")
    if nav_pattern.search(text):
        html_file.write_text(nav_pattern.sub(nav, text, count=1), encoding="utf-8")

print("Created schedule.html and administration.html.")
print("Updated intro.html and added both pages to the sidebar.")
print("Original intro.html backed up as intro.html.before-2026-2027.")
print("Existing lecture pages, notebooks, images, and theme assets were not modified.")
