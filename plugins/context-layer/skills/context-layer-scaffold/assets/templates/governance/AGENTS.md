# Agent Instructions

These instructions apply to all AI assistants working in this repository.

## Core Rules
- Always review `CHANGELOG.md` and `ROADMAP.md` before starting significant work.
- Treat `DOCS/` as the documentation source of truth.
- Treat legacy `docs/` or `documentation/` roots as migration sources, not canonical destinations.
- Update docs when code changes affect behavior, workflows, or interfaces.
- Maintain frontmatter (`title`, `description`, `status`, `lastUpdated`, `owner`).
- Keep `{{DOCS_ROOT}}/README.md` and `{{DOCS_ROOT}}/index.md` accurate.
- Treat `{{DOCS_ROOT}}/development/` as the process-doc home and `{{DOCS_ROOT}}/evidence/` as the durable audit/artifact home.
- Use checkpoint-based progress updates instead of `today/tomorrow` handoff wording.
- Generate timestamps with `node scripts/docs/timestamp-et.mjs --json` (never hand-type them).
- Prefer `DOCS/` for newly scaffolded docs roots, keep `PROJECTS/` uppercase, keep other scaffolded docs directories lowercase, and reserve uppercase markdown filenames for `README.md`, `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md`.
- Keep the reusable project template at `{{DOCS_ROOT}}/PROJECTS/NNNN_project_template.md`; lifecycle folders are for real project docs.
- Treat `{{DOCS_ROOT}}/PROJECTS/dashboard.html` as generated output and regenerate it from project docs.
- For significant user-facing UI, redesign, restyle, dashboard, app, website, form, screenshot-route, or visual QA work, use `$visual-design-critique` before implementation sign-off or movement to `in-review`.
- Each project update must include:
  - absolute timestamp (`YYYY-MM-DD HH:MM ET (America/New_York)`)
  - completed since prior checkpoint
  - next checkpoint targets

## Project Planning
- Create a numbered project doc under `{{DOCS_ROOT}}/PROJECTS/active/` at project kickoff.
- Use `projectType`, `parentProject`, and `programTrack` frontmatter to represent parent/child project relationships.
- Child projects move through lifecycle folders independently when they have separate scope, lifecycle state, evidence, risk, or review.
- Move the doc across status folders as work progresses.
- Move a project to `{{DOCS_ROOT}}/PROJECTS/in-review/` and set `status: in-review` when implementation is complete but walkthrough/sign-off has not happened yet.
- Move a project to `{{DOCS_ROOT}}/PROJECTS/blocked/` and set `status: blocked` when waiting on user decisions, permissions, access, or missing inputs.
- Do not move a project to `{{DOCS_ROOT}}/PROJECTS/completed/` until collaborative walkthrough/sign-off is complete.
- While projects are in `in-review` or `blocked`, continue execution by pulling the next prioritized backlog/stale stream.
- Reference the project number in roadmap and changelog entries.
- Maintain a checkpoint log in each project doc and add a checkpoint for major decisions, delivery milestones, or scope changes.
- Record visual design critique outcomes in the project doc for user-facing UI work, including the verdict, must-fix issues, evidence paths, and remaining approved deviations.
- Use a literal `MAGGIE TODO:` callout for Maggie-owned manual input, evidence gathering, manual testing, approval, or external workstream dependencies.
- Keep unresolved items in a `## MAGGIE TODO` section in the project doc. If those items gate progress, keep the project in `blocked/`.

## Docs Site
- Local dev: `npm --prefix docs-site run dev`
- Build: `npm --prefix docs-site run build`
- Cloudflare Pages: Root Directory repo root, Build command `npm --prefix docs-site run build`, Build output directory `{{DOCS_ROOT}}/.vitepress/dist`
