#!/usr/bin/env python3
"""Generate prayers.qmd (All Prayers page) and the _quarto.yml sidebar
from catalog.yml + the prayer .md files that actually exist.

Run before `quarto render` (the GitHub Actions workflow does this
automatically). To add a topic, edit catalog.yml. To write a prayer,
create its .md file at the path listed in catalog.yml — it appears on
the site automatically on the next build.
"""

import os
import re
import urllib.parse

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/csprayers/csprayers.com"

PRAYER_TEMPLATE = """---
title: "{title}"
author: Your Name
date: {date}
status: draft
---

*A sentence describing the moment this prayer is for*

---

> Write the prayer here,
>
> line by line,
>
> Amen.
"""


def load_catalog():
    with open(os.path.join(ROOT, "catalog.yml")) as f:
        return yaml.safe_load(f)["sections"]


def file_status(path):
    """Return 'final', 'draft', or None if the file doesn't exist."""
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return None
    with open(full) as f:
        m = re.match(r"^---\n(.*?)\n---", f.read(), re.S)
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
        return fm.get("status", "draft")
    return "draft"


def contribute_url(topic):
    fname = topic["file"]
    value = PRAYER_TEMPLATE.format(title=topic["title"], date="YYYY-MM-DD")
    q = urllib.parse.urlencode({"filename": fname, "value": value})
    return f"{REPO}/new/main?{q}"


def topic_line(topic):
    status = file_status(topic["file"])
    if status is None:
        url = contribute_url(topic)
        return (
            f'- <span class="unwritten">{topic["title"]}</span>'
            f'<a class="contribute" href="{url}" title="Contribute this prayer">contribute</a>'
        )
    href = topic["file"]
    tag = ' <span class="draft-tag">draft</span>' if status == "draft" else ""
    return f'- [{topic["title"]}]({href}){tag}'


def section_counts(sec):
    topics = list(sec.get("topics", []))
    for ss in sec.get("subsections", []):
        topics += ss.get("topics", [])
    written = sum(1 for t in topics if file_status(t["file"]) is not None)
    return written, len(topics)


def build_prayers_page(sections):
    out = [
        "---",
        "title: All Prayers",
        "subtitle: A map of moments for prayer in the life of computer science",
        "---",
        "",
        "Written prayers appear as links. The rest are moments still waiting "
        "for words — select “contribute” to write one (it opens a "
        "pre-filled editor on GitHub).",
        "",
    ]
    for sec in sections:
        written, total = section_counts(sec)
        out.append(f'## {sec["title"]}')
        out.append("")
        if sec.get("blurb"):
            out.append(f'*{sec["blurb"]}*')
            out.append("")
        for t in sec.get("topics", []):
            out.append(topic_line(t))
        if sec.get("topics"):
            out.append("")
        for ss in sec.get("subsections", []):
            out.append(f'### {ss["title"]}')
            out.append("")
            if ss.get("blurb"):
                out.append(f'*{ss["blurb"]}*')
                out.append("")
            for t in ss.get("topics", []):
                out.append(topic_line(t))
            out.append("")
    with open(os.path.join(ROOT, "prayers.qmd"), "w") as f:
        f.write("\n".join(out) + "\n")


def build_sidebar(sections):
    """Sidebar lists only written prayers, grouped by section."""
    lines = []

    def add(indent, text):
        lines.append("      " + "  " * indent + text)

    add(0, "- index.md")
    add(0, "- prayers.qmd")
    for sec in sections:
        entries = []
        for t in sec.get("topics", []):
            if file_status(t["file"]) is not None:
                entries.append((None, t))
        for ss in sec.get("subsections", []):
            for t in ss.get("topics", []):
                if file_status(t["file"]) is not None:
                    entries.append((ss["title"], t))
        if not entries:
            continue
        add(0, f'- section: "{sec["title"]}"')
        add(0, "  contents:")
        for _, t in entries:
            add(1, f'- {t["file"]}')

    sidebar_block = "\n".join(lines)
    qpath = os.path.join(ROOT, "_quarto.yml")
    with open(qpath) as f:
        cfg = f.read()
    new = re.sub(
        r"(# BEGIN GENERATED SIDEBAR[^\n]*\n).*?(\s*# END GENERATED SIDEBAR)",
        r"\1" + sidebar_block + r"\2",
        cfg,
        flags=re.S,
    )
    with open(qpath, "w") as f:
        f.write(new)


if __name__ == "__main__":
    sections = load_catalog()
    build_prayers_page(sections)
    build_sidebar(sections)
    total_written = sum(section_counts(s)[0] for s in sections)
    total = sum(section_counts(s)[1] for s in sections)
    print(f"Generated prayers.qmd and sidebar: {total_written} written of {total} topics.")
