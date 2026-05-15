---
name: checkpoint-log
description: Use when asked to add an ET-timestamped checkpoint, handoff, progress update, completed-work summary, or next checkpoint target.
---

# Checkpoint Log

Use this skill to write durable project progress updates.

## First Checks

1. Locate the owning project doc under `DOCS/PROJECTS/`.
2. Run `node scripts/docs/timestamp-et.mjs --json` to get the timestamp.
3. Read the latest checkpoint to avoid duplicating prior notes.

If `scripts/docs/timestamp-et.mjs` is missing, offer to run `$context-layer-scaffold`.

## Format

Add a new checkpoint entry:

```md
### Checkpoint NN - YYYY-MM-DD HH:MM ET (America/New_York)
#### Completed Since Prior Checkpoint
- ...

#### Next Checkpoint Targets
- ...

#### Notes
- ...
```

## Rules

- Do not use `today`, `tomorrow`, or relative-date handoff headings.
- Include evidence paths, risks, open questions, and `MAGGIE TODO:` callouts when relevant.
- If the checkpoint changes lifecycle state, use `$project-lifecycle` rules.
- If the checkpoint records user-facing UI readiness, include the visual design gate outcome when required.
