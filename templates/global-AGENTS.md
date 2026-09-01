# Global Agent Policy

These rules apply on this workstation unless a repository provides narrower, compatible instructions.

## Protected actions

- Do not purchase, subscribe, transfer funds, or otherwise create a financial commitment without explicit approval in the current task for the exact action and target.
- Do not delete material local or remote data without explicit approval in the current task for the exact target. Prefer reversible operations and resolve the exact target first.
- Do not send, post, submit, or otherwise transmit external correspondence without explicit approval in the current task for the exact message and recipient.
- Broad or standing autonomy is not approval for a protected action. If scope is unclear, stop before the action and ask.
- Read-only analysis, diagnostics, and drafts are allowed. An explicitly approved correspondence automation may act only inside its written scope and may never spend money or delete data.

## Two-workstation operation

- Git is the source of truth for project code, durable context, and handoffs. Never sync Git working directories, `.env` files, plugin caches, or automation state through consumer file-sync services.
- Use one owner per task branch at a time. Before switching workstations, commit and push a named checkpoint; the receiving workstation must pull and verify the exact commit.
- Resolve committed paths from the repository root. Do not commit workstation-specific usernames or absolute home-directory paths.
- Keep credentials, caches, logs, indexes, and host-bound application state local. Never print or commit secret values.
- The MacBook Pro is the primary interactive/orchestration host. The MacBook Air is the operations host for explicitly assigned, credential-bound automations. Do not activate duplicate live automations.

## Instruction hygiene

- Repository `AGENTS.md` files remain authoritative for project-specific behavior.
- Treat `AGENTS.override.md` as exceptional and temporary. Surface every discovered override for review.
- Preserve unrelated user changes and stop before reset, discard, destructive cleanup, or conflict resolution that could lose work.
