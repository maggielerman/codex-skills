# Verification

Run this checklist before finishing.

## Required Baseline

- `DOCS/` exists and is canonical.
- `DOCS/README.md` exists.
- `DOCS/index.md` exists.
- `DOCS/PROJECTS/README.md` exists.
- `DOCS/PROJECTS/NNNN_project_template.md` exists.
- Lifecycle folders exist under `DOCS/PROJECTS/`.
- `DOCS/development/checkpoint-workflow.md` exists.
- `DOCS/development/visual-design-quality-gate.md` exists.
- `DOCS/evidence/README.md` exists.
- `DOCS/evidence/active/`, `archive/`, and `templates/` exist.
- `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md` exist or were safely updated.
- `scripts/docs/manifest.mjs`, `check-links.mjs`, `normalize-frontmatter.mjs`, and `timestamp-et.mjs` exist.
- `scripts/docs/projects-dashboard.mjs` exists.
- `DOCS/PROJECTS/dashboard.html` exists.
- `DOCS/PROJECTS/README.md` links to `dashboard.html`.

## Commands

When prerequisites exist, run:

```bash
node scripts/docs/manifest.mjs DOCS
node scripts/docs/check-links.mjs DOCS
```

If `package.json` scripts were added, also verify:

```bash
npm run docs:manifest
npm run docs:links
```

If the dashboard was generated, verify:

- links point to Markdown project docs
- templates are skipped
- blocked and in-review items are visible
- unresolved `MAGGIE TODO:` items appear in a dedicated section
- parent/child groupings appear when frontmatter exists

## Optional Module Checks

If UX/UI bug intake is enabled:

- `DOCS/ux-ui-bugs/README.md` exists.
- `DOCS/ux-ui-bugs/INBOX.md` exists.
- `DOCS/ux-ui-bugs/TRIAGED.md` exists.
- `DOCS/ux-ui-bugs/ARCHIVE.md` exists.
- Governance/docs indexes link or mention the bug intake workflow.
- Durable bug evidence is directed to `DOCS/evidence/active/<project-id>/ux-ui-bugs/<bug-id>/`.

## Final Report

Report:

- created files
- updated files
- skipped existing files
- blocked or unsafe operations
- old docs roots found
- `MAGGIE TODO:` items added
- verification commands run and their outcomes
