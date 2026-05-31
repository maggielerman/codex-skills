---
name: project-dashboard
description: Use when asked to generate, repair, or inspect DOCS/PROJECTS/dashboard.html, blocked/in-review queues, Maggie TODO rollups, or status drift.
---

# Project Dashboard

Use this skill for the generated dashboard at `DOCS/PROJECTS/dashboard.html`.

## First Checks

1. Locate `DOCS/PROJECTS/`.
2. Confirm `scripts/docs/projects-dashboard.mjs` exists.
3. Confirm project docs live in lifecycle folders.

If the dashboard generator is missing, offer to run `$context-layer-scaffold` or install the required dashboard baseline.

## Generate

Run:

```bash
node scripts/docs/projects-dashboard.mjs DOCS
```

If `package.json` contains `docs:projects-dashboard`, this is also acceptable:

```bash
npm run docs:projects-dashboard
```

## Validate

Check that:

- `DOCS/PROJECTS/dashboard.html` exists
- links open project Markdown docs
- `README.md` and `NNNN_project_template.md` are skipped
- blocked and in-review items are visible
- unresolved `MAGGIE TODO:` items appear in a dedicated section
- optional content calendar appears when `DOCS/content/content-calendar.json`, `DOCS/content/blog-content-calendar.json`, or another `DOCS/content/*calendar*.json` file exists
- `parentProject` and `programTrack` fields produce grouping
- status drift is surfaced when frontmatter differs from folder lane

Treat the dashboard as generated output. The Markdown project docs remain the source of truth.
