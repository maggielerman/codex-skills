---
name: collaborative-walkthrough
author: Maggie Lerman
description: Run a structured Q&A walkthrough for in-review project streams in repos with standardized docs scaffolding. Use when a user asks for collaborative walkthrough, sign-off review, or readiness check before moving projects to completed.
---

# Collaborative Walkthrough

## Overview

Use this skill to review all `in-review` project docs, surface outstanding risks/decisions, and ask focused sign-off questions. Do not move projects to `completed` until the user explicitly approves each stream.

## When To Use

- User asks for a collaborative walkthrough.
- User asks if in-review streams are ready for sign-off.
- User wants a Q&A pass that highlights unresolved decisions and risk before closure.

## Required Behavior

- Never auto-transition `in-review` projects to `completed`.
- Present evidence-backed findings first, then ask concise sign-off questions.
- Call out anything requiring user input, approval, or policy decision.
- If user approvals are partial, only transition approved streams.

## Workflow

1. Detect docs scaffold.
- Prefer `docs/` if present, otherwise `DOCS/`.
- Confirm `PROJECTS/in-review` exists and enumerate project docs.

2. Build a per-project review register.
- Frontmatter: `title`, `status`, `lastUpdated`, `owner`.
- Latest checkpoint timestamp.
- Open `Risks` and `Open Questions`.
- Outstanding “Next Checkpoint Targets”.
- Dependencies/blockers/gates mentioned in doc text.

3. Evaluate readiness and classify each project.
- `ready-for-signoff`: no unresolved blockers and no critical unanswered decisions.
- `needs-user-input`: one or more user decisions required.
- `follow-up-needed`: technical/documentation gaps should be addressed before sign-off.

4. Produce collaborative Q&A packet.
- Use the output contract below.
- Ask direct, decision-oriented questions.
- Keep question count lean (typically 1-3 per project).

5. Execute lifecycle moves only after explicit approval.
- For each approved project: add completion checkpoint, set `status: completed`, move file to `PROJECTS/completed/`.
- Update `ROADMAP.md` and `CHANGELOG.md`.
- Run docs sync checks (`docs:frontmatter`, `docs:manifest`, `docs:links`) if scripts exist.

## Output Contract

Return sections in this order:
1. `Walkthrough Status`
2. `Project Readiness Matrix`
3. `What Needs Your Input`
4. `Recommended Actions Before Sign-Off`
5. `Sign-Off Questions`

For each project in the matrix include:
- project id/title
- readiness class (`ready-for-signoff`, `needs-user-input`, `follow-up-needed`)
- 1-3 evidence bullets with file references

## Repo Conventions

- Use absolute timestamps in ET for checkpoint logs when repo governance requires it.
- If repo provides `scripts/docs/timestamp-et.mjs`, use it for timestamps.
- Keep lifecycle state consistent between folder location and frontmatter `status`.

## References

- Use [references/question-bank.md](references/question-bank.md) to generate concise, high-signal walkthrough questions.
