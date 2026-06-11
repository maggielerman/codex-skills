---
name: context-layer-dashboard-backfill
description: Custom skill created by Maggie Lerman. Backfill or refresh the modern Context Layer generated project dashboard in existing repositories that already have DOCS/PROJECTS lifecycle folders. Use when a repo needs the sidebar-based dashboard.html, All Projects register, MAGGIE TODO rollup, status drift, program tracks, and optional content calendar without rerunning the broader context-layer scaffold.
---

# Context Layer Dashboard Backfill

Custom skill created by Maggie Lerman.

Use this skill to update an existing repo to the modern generated Context Layer project dashboard without rerunning the full scaffold.

## When To Use

Use this skill when:

- the repo already has a docs root such as `DOCS/`, `docs/`, or `documentation/`
- project docs already live under `PROJECTS/active/`, `PROJECTS/in-review/`, `PROJECTS/blocked/`, `PROJECTS/completed/`, `PROJECTS/backlog/`, or `PROJECTS/stale/`
- the user wants the current sidebar-based `dashboard.html` in existing repos
- the user asks to backfill, refresh, upgrade, or standardize project dashboards across existing context-layer repos

Do not use this skill for greenfield docs setup. If the repo does not already have a `PROJECTS/` lifecycle tree, use `$context-layer-scaffold` or `$product-operating-system-scaffold` first.

## Dashboard Contract

The generated dashboard must keep the existing Context Layer data contract:

- `Portfolio Snapshot`
- `Attention Queue`
- `MAGGIE TODO`
- `Program Tracks`
- `Recently Updated`
- `Status Drift`
- `All Projects`
- optional `Content Calendar`

Do not invent new source sections, new project metrics, cloud collaboration features, or external workflow assumptions.

The source of truth remains the Markdown project docs. `PROJECTS/dashboard.html` is generated output.

Read [references/dashboard-contract.md](references/dashboard-contract.md) only when changing the dashboard extraction or output contract.

## Backfill Workflow

1. Inspect the target repo.
   - Confirm the docs root and `PROJECTS/` lifecycle folders.
   - Check `git status --short` before writing.
   - If multiple docs roots exist and the right one is ambiguous, ask before installing.

2. Run the bundled installer.

```bash
python3 "$SKILL_ROOT/scripts/install_docs_project_dashboard.py" \
  --repo /absolute/path/to/repo \
  --docs-root DOCS
```

If the repo already has a generated dashboard and the user explicitly wants to replace it, use:

```bash
python3 "$SKILL_ROOT/scripts/install_docs_project_dashboard.py" \
  --repo /absolute/path/to/repo \
  --docs-root DOCS \
  --force-dashboard
```

If the repo also needs starter content-calendar files, add `--with-content-calendar`.

3. Verify the generated dashboard.
   - Confirm `DOCS/PROJECTS/dashboard.html` exists.
   - Confirm the sidebar views are present.
   - Confirm the `All Projects` table searches and filters.
   - Confirm `All Projects` uses an internal scroll container instead of endless page scroll.
   - Confirm project doc links are relative and open the underlying Markdown files.
   - Confirm blocked, in-review, active, `MAGGIE TODO`, program tracks, status drift, and optional content calendar sections render from existing data.

4. Run repo-local docs checks when available.
   - `npm run docs:projects-dashboard`
   - `npm run docs:manifest`
   - `npm run docs:links`
   - `git diff --check`

Skip missing scripts; report what was unavailable.

## Safety

- Do not rewrite project docs to make the dashboard prettier.
- Do not change lifecycle folder placement unless the user explicitly asks.
- Do not overwrite a non-generated `PROJECTS/dashboard.html` without explicit permission.
- Preserve unrelated dirty worktree changes.
- Treat content calendar starter files as optional; do not install them unless requested.

## Resources

- Installer: `scripts/install_docs_project_dashboard.py`
- Dashboard generator asset: `assets/repo/scripts/docs/projects-dashboard.mjs`
- Optional content calendar templates: `assets/repo/docs/content/content-calendar.{json,md}`
- Dashboard contract: `references/dashboard-contract.md`
