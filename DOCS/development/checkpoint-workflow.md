---
title: Checkpoint Workflow
description: Timestamped checkpoint standard for continuous execution docs
status: stable
lastUpdated: "2026-04-28 12:04 ET (America/New_York)"
owner: Product/Engineering
---

# Checkpoint Workflow

Use this standard for project execution updates across roadmap, project docs, and changelog entries.

## Timestamp Source (Required)

Always generate timestamps with:

```bash
node scripts/docs/timestamp-et.mjs --json
```

Use `timestampEt` from script output. Do not hand-type date/time values.

## Timestamp Format

- `YYYY-MM-DD HH:MM ET (America/New_York)`
- Example: `2026-02-11 14:37 ET (America/New_York)`

## Checkpoint Entry Structure

For each checkpoint, include:

1. Checkpoint title and timestamp
2. Completed since prior checkpoint
3. Next checkpoint targets
4. Optional notes (context, risks, links)

## Anti-Pattern

- Avoid `today/tomorrow` handoff sections.
