# Project Dashboard

The project dashboard is required baseline scaffold output.

## Required Behavior

Install or update:

- `scripts/docs/projects-dashboard.mjs`
- `DOCS/PROJECTS/dashboard.html`
- `DOCS/PROJECTS/README.md` link to `dashboard.html`

When `package.json` exists, add:

- `docs:projects-dashboard`: `node scripts/docs/projects-dashboard.mjs DOCS`

Run the existing dashboard installer:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/docs-project-dashboard-legacy/scripts/install_docs_project_dashboard.py" \
  --repo . \
  --docs-root DOCS
```

If package infrastructure is absent, run the generator directly after installing it:

```bash
node scripts/docs/projects-dashboard.mjs DOCS
```

## Safety

- Treat `dashboard.html` as generated output.
- Markdown project docs remain the source of truth.
- If an older generated `dashboard.md` exists, it may be removed by the installer.
- If a non-generated `DOCS/PROJECTS/dashboard.html` exists, stop and ask before replacing it.

## Dashboard Must Surface

- portfolio snapshot by lifecycle lane
- attention queue
- blocked and in-review work
- `MAGGIE TODO:` items
- program tracks
- parent/child project grouping
- status drift between folder lane and frontmatter
- full project register with links to Markdown docs

The dashboard should skip `README.md` and `NNNN_project_template.md`.
