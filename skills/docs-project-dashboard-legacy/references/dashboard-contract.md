# Dashboard Contract

Use this reference when changing the generated HTML dashboard structure.

## Purpose

The dashboard is a generated HTML portfolio view for docs-native project planning systems. It should help the user scan the whole portfolio quickly, then click through to the planning docs for detail.

## Input Assumptions

- The repo already has a docs root at `DOCS/`, `docs/`, or `documentation/`.
- Project docs live under `PROJECTS/` lifecycle folders.
- Each project doc is a markdown file with frontmatter when available.
- Project docs may include literal `MAGGIE TODO:` callouts for manual follow-up that should be surfaced in the dashboard.
- Common frontmatter fields:
  - `title`
  - `description`
  - `status`
  - `priority`
  - `lastUpdated`
  - `owner`
  - `parentProject`
  - `programTrack`

## Extraction Rules

- Treat lifecycle folder placement as the canonical lane.
- Skip:
  - `README.md`
  - `NNNN_project_template.md`
- Extract project id from the filename prefix first, then fall back to the title.
- Extract the first bullet list under the most recent `#### Next Checkpoint Targets` block when present.
- Count bullets in `## Risks` and `## Open Questions` when present.
- Extract unresolved `MAGGIE TODO:` callouts anywhere in the file and de-duplicate identical lines within a project.
- Detect status drift when normalized frontmatter `status` does not match the lifecycle folder.

## Required Sections

1. `Portfolio Snapshot`
2. `Attention Queue`
3. `Maggie TODO`
4. `Program Tracks`
5. `Recently Updated`
6. `Status Drift`
7. `Full Register`

## Required Behaviors

- Include links to the underlying planning docs.
- Keep `blocked`, `in-review`, and `active` highly visible.
- Surface unresolved `MAGGIE TODO:` items in their own dashboard section with links back to the owning project docs.
- Group child streams when `parentProject` or `programTrack` is present.
- Sort `Recently Updated` descending by parsed `lastUpdated`.
- Keep the page self-contained so it opens locally without a build step.
- Prefer a static HTML file with embedded CSS and light client-side filtering over markdown tables.
- Mark the dashboard as generated so future runs can safely replace it.

## Output Notes

- The dashboard file path is `PROJECTS/dashboard.html`.
- Do not emit a markdown dashboard export.
- The file should say how to regenerate it.
- Relative links should be rooted from `PROJECTS/dashboard.html`.
