# Baseline Scaffold

Use this reference for the required scaffold path.

## Docs Root

`DOCS/` is always canonical. For new repos, create `DOCS/`. For existing repos with `docs/` or `documentation/`, treat those roots as migration sources and use `DOCS/` as the destination. Do not preserve lowercase or legacy roots as the operating system target.

If old roots contain unique content, do not delete them automatically. Copy or merge only when it is safe, and report unresolved migration choices.

## Required Files

Create or update these baseline files:

- `DOCS/README.md`
- `DOCS/index.md`
- `DOCS/PROJECTS/README.md`
- `DOCS/PROJECTS/NNNN_project_template.md`
- `DOCS/development/checkpoint-workflow.md`
- `DOCS/development/visual-design-quality-gate.md`
- `DOCS/evidence/README.md`
- `DOCS/historical/index.md`

Also create topic placeholders when missing:

- `DOCS/api/index.md`
- `DOCS/contributing/index.md`
- `DOCS/database/index.md`
- `DOCS/deployment/index.md`
- `DOCS/development/index.md`
- `DOCS/features/index.md`
- `DOCS/getting-started/index.md`

## Required Folders

Project lifecycle folders:

- `DOCS/PROJECTS/active/`
- `DOCS/PROJECTS/in-review/`
- `DOCS/PROJECTS/blocked/`
- `DOCS/PROJECTS/completed/`
- `DOCS/PROJECTS/backlog/`
- `DOCS/PROJECTS/stale/`

Evidence folders:

- `DOCS/evidence/active/`
- `DOCS/evidence/archive/`
- `DOCS/evidence/templates/`

## Placeholder Replacement

When copying templates, replace:

- `{{DOCS_ROOT}}` -> `DOCS`
- `{{LAST_UPDATED_DATE_ET}}` -> `dateEt` from `timestamp-et.mjs`
- `{{LAST_UPDATED_TS_ET}}` -> `timestampEt` from `timestamp-et.mjs`
- `{{PROJECT_NAME}}` -> repo directory name

## Docs Tooling

Copy the bundled scripts into `scripts/docs/`:

- `manifest.mjs`
- `check-links.mjs`
- `normalize-frontmatter.mjs`
- `timestamp-et.mjs`

If `package.json` exists, add missing scripts only:

- `docs:manifest`: `node scripts/docs/manifest.mjs DOCS`
- `docs:links`: `node scripts/docs/check-links.mjs DOCS`
- `docs:frontmatter`: `node scripts/docs/normalize-frontmatter.mjs DOCS`
- `docs:timestamp`: `node scripts/docs/timestamp-et.mjs --json`

Do not assume npm CI support exists just because docs scripts exist.
