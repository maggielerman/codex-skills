---
name: collaborative-walkthrough
description: Use when asked for in-review Context Layer walkthroughs, readiness reviews, sign-off Q&A, or completion approval before moving projects to completed.
---

# Collaborative Walkthrough

Use this skill as the human sign-off gate for `DOCS/PROJECTS/in-review/` streams before moving work to `completed/`.

## First Checks

1. Locate `DOCS/PROJECTS/in-review/`.
2. Read `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`, and `DOCS/PROJECTS/README.md` when present.
3. Enumerate in-review project docs.
4. Include child projects and parent rollups when `parentProject` or `programTrack` is present.

If no `in-review/` folder exists, offer to run `$context-layer-scaffold`.

## Required Behavior

- Never auto-transition projects to `completed`.
- Present evidence-backed readiness findings first.
- Ask concise sign-off questions.
- Call out missing evidence, blockers, unresolved `MAGGIE TODO:` items, and policy decisions.
- Only transition streams after explicit user approval.
- If approvals are partial, transition only approved streams.

## Readiness Classes

- `ready-for-signoff`: no unresolved blockers, no critical unanswered decisions, evidence is linked.
- `needs-user-input`: Maggie or another human must decide, approve, test, or provide input.
- `follow-up-needed`: technical, documentation, evidence, or verification gaps should be addressed first.

## Approval Actions

For each approved project:

1. Generate an ET timestamp with `node scripts/docs/timestamp-et.mjs --json`.
2. Add a completion checkpoint.
3. Set frontmatter `status: completed`.
4. Move the file to `DOCS/PROJECTS/completed/`.
5. Update `ROADMAP.md` and `CHANGELOG.md`.
6. Regenerate the project dashboard.
7. Run docs checks when available.

## Output Contract

Return sections in this order:

1. `Walkthrough Status`
2. `Project Readiness Matrix`
3. `What Needs Your Input`
4. `Recommended Actions Before Sign-Off`
5. `Sign-Off Questions`

For each project include id/title, readiness class, and 1-3 evidence bullets with file references.
