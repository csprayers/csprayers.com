# Prayers for Computer Science

A collection of prayers for those who study, teach, and practice the craft of computing.

## About

This website offers prayers for every season, struggle, and celebration in the life of computer science students and professors. From the first day of class to defending a thesis, from debugging frustrating code to experiencing breakthrough moments, these prayers invite us to bring our whole selves before God.

## How the Site Works

The site is built with [Quarto](https://quarto.org). Two kinds of content drive it:

- **Prayer files** (`*.md` in the numbered section folders) — one file per *written* prayer. Only written prayers have files.
- **`catalog.yml`** — the complete map of all planned prayer topics (sections, subsections, blurbs, titles).

At build time, `scripts/build_index.py` (run automatically by `quarto render` as a pre-render step) compares the catalog with the files on disk and generates:

- `prayers.qmd` — the All Prayers page: written prayers are links; unwritten topics appear muted, each with a "contribute" link that opens a pre-filled editor on GitHub.
- The sidebar in `_quarto.yml` (between the `GENERATED SIDEBAR` markers) — listing only written prayers.

Deployment is via GitHub Actions (`.github/workflows/deploy.yml`) to GitHub Pages on every push to `main`.

## Contributing (for visitors)

Visitors contribute through the **Contribute** page on the site — a form (backed by [Formspree](https://formspree.io)) that emails each submission to the curator. The "contribute" links on the All Prayers page pre-fill the form with the topic. No GitHub account needed.

When a good submission arrives by email, create the prayer file for it (see below) and push.

## Writing a New Prayer (for maintainers)

1. Find the topic in `catalog.yml` and note its `file:` path.
2. Create that file:

   ```markdown
   ---
   title: "The Title of the Prayer"
   author: Your Name
   date: 2026-07-04
   status: draft        # or: final
   ---

   *A sentence describing the moment this prayer is for*

   ---

   > The prayer itself,
   >
   > written line by line as blockquotes,
   >
   > Amen.
   ```

3. Commit and push (or open a pull request). The site rebuilds itself — the new prayer appears in the sidebar and becomes a link on the All Prayers page automatically.

To add a brand-new topic, add an entry to `catalog.yml`.

## Local Development

Requires [Quarto](https://quarto.org/docs/get-started/) and Python 3 with `pyyaml`.

```bash
quarto preview     # local dev server
quarto render      # build into _site/
```

## Prayer Writing Guidelines

- Prayers should be appropriate for both students and professors
- Use inclusive language
- Be honest about struggle and doubt
- Root prayers in hope and the character of God
- Consider the specific CS context

## Project Structure

```
csprayers.com/
├── _quarto.yml           # Quarto site config (sidebar section is generated)
├── catalog.yml           # Map of all prayer topics, written and unwritten
├── scripts/
│   └── build_index.py    # Generates prayers.qmd + sidebar from catalog.yml
├── theme/
│   ├── liturgy.scss      # Site theme (colors, typography)
│   ├── logo.svg          # Logo source (icon.png is rendered from it)
│   └── front.svg         # Front-page art source (front.png)
├── index.md              # Homepage
├── 1-academic-year/      # Written prayers, one .md file each,
├── 2-learning/           #   organized by section
└── ...
```

## License

MIT License - see LICENSE file for details

## Acknowledgments

This project was inspired by the need for resources that integrate faith with the study and practice of computer science.
