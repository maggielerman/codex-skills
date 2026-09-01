# MacBook Air Baseline Apply — Phase 2

Recorded: 2026-09-01 04:46 ET (America/New_York)

## Scope and history

- Worktree: `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills`
- Branch: `codex/air-baseline-apply`
- The doctor policy-file fix `c613c052d02c1dcda4fb7f30f46385b2d68c0b2d` was fetched and cherry-picked without reset or history rewriting.
- Cherry-picked Air commit: `188b233` (`Fix global policy doctor validation`).
- The existing migration worktree and branch were not modified.
- Existing plugin registrations and installed user state were preserved.

## Apply result

The workstation bootstrap ran in preview mode and then applied using the existing ignored Air host overlay, this time with plugin handling enabled. The bootstrap created another recoverable backup at:

`/Users/maggielerman/.codex/backups/workstation-bootstrap/20260901T084614815518Z`

The apply performed these plugin actions:

1. Registered `custom-plugin-backups` at `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills`.
2. Installed and enabled Working Modes 0.1.0 from the Git-backed baseline package.
3. Installed and enabled Motion Design Director 0.1.0 from the Git-backed baseline package.
4. Left the existing Context Layer, RPS Etsy Ops, and Multi-Mailbox Ops installations unchanged.

No plugin was removed, replaced, disabled, or upgraded. The baseline Context Layer and RPS packages became available through the new marketplace but were not installed over their existing home-local registrations.

## Registered custom marketplaces

| Marketplace | Root |
|---|---|
| `home-local` | `/Users/maggielerman` |
| `custom-plugin-backups` | `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills` |
| `multi-mailbox-ops-local` | `/Users/maggielerman/Github/multi-mailbox-ops` |

## Exact configured plugin IDs and effective state

| Plugin ID | Configured | Effective state | Active source |
|---|---:|---|---|
| `context-layer@home-local` | Enabled | Installed and enabled, version 0.1.0; unchanged | `/Users/maggielerman/plugins/context-layer` |
| `rps-etsy-ops@home-local` | Enabled | Installed and enabled, version 0.1.0; unchanged | `/Users/maggielerman/plugins/rps-etsy-ops` |
| `working-modes@custom-plugin-backups` | Enabled | Installed and enabled, version 0.1.0 | `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills/plugins/working-modes` |
| `motion-design-director@custom-plugin-backups` | Enabled | Installed and enabled, version 0.1.0 | `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills/plugins/motion-design-director` |
| `multi-mailbox-ops@multi-mailbox-ops-local` | Enabled | Installed and enabled, version 0.1.0; unchanged | `/Users/maggielerman/Github/multi-mailbox-ops/plugins/multi-mailbox-ops` |

The installed configuration contains no second Context Layer or RPS plugin ID. Their Git-backed baseline packages are available but disabled candidates, which preserves the existing home-local registrations without duplicating installed state.

## Verification

- Full repository tests: 17 passed, zero failures.
- Global policy: pass, exact digest `9d52b928b5ae2544558e1bb8685e0f2fe93617a1f0a5d1e68379aa7d42af3e24`, installed mode `600`.
- All 12 selected direct skills: pass with exact source-tree digests.
- Working Modes: pass; version, enabled state, and source-tree digest match.
- Motion Design Director: pass; version, enabled state, and source-tree digest match.
- Multi-Mailbox Ops: pass; version, enabled state, and source-tree digest remain unchanged and exact.

The workstation doctor correctly returned overall `drift` because two deliberately preserved home-local source trees do not yet match the baseline packages:

| Remaining drift | Expected baseline digest | Active digest | State |
|---|---|---|---|
| Context Layer | `c8ff6322e383cf29d73b9126e938a066ae15c6794a1bf54887bcbe9dba6f9331` | `1b6c852f0ecbaf080c621abe5fb7d73b19e29ba3b8ad51e5abab14e390f56872` | Version 0.1.0 and enabled state match; source tree differs. |
| RPS Etsy Ops | `e287f8b3da64fb7868b675d6be9bb493c2c4af7ab4b03f044d2cb72f3e00a4aa` | `101c427f411299cef2fdc39b34ec5b2561016b86a23ad5a97edfed0c1e5bd8e3` | Version 0.1.0 and enabled state match; source tree differs. |

There is no remaining policy, direct-skill, Working Modes, Motion, or MMO drift.

## Boundary for a later phase

Replacing or repointing Context Layer and RPS Etsy Ops is intentionally deferred. Any later change should resolve the exact package targets, preserve their current registrations with a recoverable backup, apply one plugin at a time, and read back the effective plugin ID, enabled state, version, and source digest before proceeding.

Plugin caches remain installation evidence only and are not source authority.
