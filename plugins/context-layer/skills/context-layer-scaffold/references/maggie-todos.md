# MAGGIE TODO

`MAGGIE TODO:` is a literal callout for Maggie-owned or externally gated work.

Use it when progress depends on:

- Maggie's manual input
- manual testing
- evidence gathering
- approval or taste sign-off
- external workstreams
- credentials, permissions, or access
- missing decisions

## Format

Use one unresolved item per line:

```md
- MAGGIE TODO: Confirm production credentials for final verification.
```

Keep unresolved items in a dedicated project-doc section:

```md
## MAGGIE TODO
- MAGGIE TODO: Capture the missing manual action here.
```

Repeat the same callout near a checkpoint, risk, dependency, or decision section when useful for context.

If unresolved `MAGGIE TODO` items block progress, move the project doc to `DOCS/PROJECTS/blocked/` and set `status: blocked`.

The project dashboard must surface unresolved `MAGGIE TODO:` items in a dedicated section.
