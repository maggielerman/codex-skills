# Agent Instructions

These instructions apply to all AI assistants working in this repository.

## Core Rules
- Always review `CHANGELOG.md` and `ROADMAP.md` before starting significant work.
- Treat the docs root (`DOCS/` or `docs/`) as the documentation source of truth.
- Update docs when code changes affect behavior, workflows, or interfaces.
- Maintain frontmatter (`title`, `description`, `status`, `lastUpdated`, `owner`).
- Keep `{{DOCS_ROOT}}/README.md` and `{{DOCS_ROOT}}/index.md` accurate.
- Use checkpoint-based progress updates instead of `today/tomorrow` handoff wording.
- Generate timestamps with `node scripts/docs/timestamp-et.mjs --json` (never hand-type them).
- Each project update must include:
  - absolute timestamp (`YYYY-MM-DD HH:MM ET (America/New_York)`)
  - completed since prior checkpoint
  - next checkpoint targets

## Project Planning
- Create a numbered project doc under `{{DOCS_ROOT}}/PROJECTS/active/` at project kickoff.
- Move the doc across status folders as work progresses.
- Move a project to `{{DOCS_ROOT}}/PROJECTS/in-review/` and set `status: in-review` when implementation is complete but walkthrough/sign-off has not happened yet.
- Move a project to `{{DOCS_ROOT}}/PROJECTS/blocked/` and set `status: blocked` when waiting on user decisions, permissions, access, or missing inputs.
- Do not move a project to `{{DOCS_ROOT}}/PROJECTS/completed/` until collaborative walkthrough/sign-off is complete.
- While projects are in `in-review` or `blocked`, continue execution by pulling the next prioritized backlog/stale stream.
- Reference the project number in roadmap and changelog entries.
- Maintain a checkpoint log in each project doc and add a checkpoint for major decisions, delivery milestones, or scope changes.

## Docs Site
- Local dev: `npm --prefix docs-site run dev`
- Build: `npm --prefix docs-site run build`
- Cloudflare Pages: Root Directory repo root, Build command `npm --prefix docs-site run build`, Build output directory `{{DOCS_ROOT}}/.vitepress/dist`
