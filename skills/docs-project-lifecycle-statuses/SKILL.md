---
name: docs-project-lifecycle-statuses
description: Custom skill created by Maggie Lerman. Transitional legacy patch for repositories that were scaffolded before product-operating-system-scaffold included `in-review` and `blocked` lifecycle states. Use only to retrofit those states and synchronized governance updates across project docs and instruction files.
---

# Docs Project Lifecycle Statuses

Custom skill created by Maggie Lerman.

Apply post-scaffold lifecycle retrofits for repositories that already have standardized docs governance (`DOCS/`, `docs/`, or `documentation/` with `PROJECTS/`) but are missing `in-review` and `blocked`.

Deprecation plan: once all active repositories have been migrated and `product-operating-system-scaffold` adoption is universal, retire this skill.

Path matching rule: treat folder/file names case-insensitively while preserving the repository's actual casing in written output.

## Workflow

1. Run the lifecycle extension script from the target repository root:

```bash
python <skill_dir>/scripts/apply_lifecycle_extension.py --repo .
```

2. Confirm these folders now exist under the docs root:
- `PROJECTS/in-review/`
- `PROJECTS/blocked/`

3. Confirm lifecycle guidance was updated in the primary instruction files:
- `AGENTS.md`
- `<docs_root>/README.md`
- `<docs_root>/index.md`
- `<docs_root>/PROJECTS/README.md`
- `README.md` (when present)

4. Confirm optional instruction-file updates when these files exist:
- `.github/copilot-instructions.md`
- `CLAUDE.md`
- `.cursor/rules/*`
- root-level `llms*.txt|md` instruction files (do not edit application route source files)

5. Rebuild docs manifest when available:

```bash
node scripts/docs/manifest.mjs <docs_root>
```

## Lifecycle Rules

- Start each new project doc in `PROJECTS/active/` with `status: active`.
- Move a project to `PROJECTS/in-review/` with `status: in-review` after end-to-end execution is complete but before user walkthrough/sign-off.
- Keep in-review projects parked while continuing autonomous execution from backlog/paused work.
- Move a project to `PROJECTS/blocked/` with `status: blocked` when progress depends on user decision, permission, access, or missing input.
- For blocked transitions, add a checkpoint entry that states:
  - blocker detail
  - who/what is needed to unblock
  - next checkpoint target after unblock
- Move to `PROJECTS/completed/` only after collaborative review/sign-off.
- Keep checkpoint formatting unchanged and always generate timestamps via `node scripts/docs/timestamp-et.mjs --json`.

## Resources

- Policy details: `references/lifecycle-policy.md`
- Deterministic updater: `scripts/apply_lifecycle_extension.py`
