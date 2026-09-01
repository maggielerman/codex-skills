# MacBook Air Baseline Apply — Phase 1

Recorded: 2026-09-01 04:37 ET (America/New_York)

## Scope and source

- Baseline source: `origin/codex/two-mac-baseline` at `32e04d1425f29f799929eb5ad2c940f4b166fb10`.
- Apply branch: `codex/air-baseline-apply`.
- Isolated worktree: `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills`.
- Existing migration checkout and branch under `/Users/maggielerman/Github/codex-skills` were preserved and were not modified by this phase.
- Ignored host overlay: `config/host-overlay.local.json`, with stable host ID `macbook-air-operations` and role `air`.

The overlay resolves these repository roots:

- `codex-skills`: `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills`
- `multi-mailbox-ops`: `/Users/maggielerman/Github/multi-mailbox-ops`
- `hyphenomenon`: `/Users/maggielerman/Github/hyphenomenon`
- `shopify-headless`: `/Users/maggielerman/Github/shopify-headless`
- `aerial-platform`: `/Users/maggielerman/Github/aerial-platform`
- `chronicle-visualizer`: `/Users/maggielerman/Documents/chronicle-visualizer`

## Applied state

The workstation bootstrap ran in preview mode, then applied with `--skip-plugins`. It changed only the global Codex policy and the 12 baseline-selected direct skills. Existing installed copies were preserved at:

`/Users/maggielerman/.codex/backups/workstation-bootstrap/20260901T083611133758Z`

The backup contains the previous global policy and the prior versions of all 12 selected direct skills.

Independent file hashing confirmed that the installed global policy exactly matches `templates/global-AGENTS.md`:

`9d52b928b5ae2544558e1bb8685e0f2fe93617a1f0a5d1e68379aa7d42af3e24`

The doctor passed every selected direct skill:

1. `artifact-template-rps-8x10-gallery-sleeve-package`
2. `catalog-review`
3. `context-layer-dashboard-backfill`
4. `hyphenomenon-chat-intake`
5. `hyphenomenon-project-intake`
6. `hyphenomenon-codex-usage-report`
7. `rps-print-order`
8. `alpinejs-lightweight-js`
9. `eleventy-jamstack-expert`
10. `jamstack-version-auditor`
11. `tailwindcss-expert`
12. `project-tranche-orchestrator`

Bootstrap and doctor unit tests also passed: four tests, zero failures.

## Doctor result

Overall doctor status was `drift` only because plugin installation was intentionally skipped.

| Capability | Expected | Observed | Result |
|---|---|---|---|
| Global policy | Baseline policy | Exact independent SHA-256 match | Pass |
| 12 direct skills | Baseline trees | All exact | Pass |
| Context Layer | 0.1.0, enabled, baseline source tree | 0.1.0 enabled from older home-local tree | Drift |
| RPS Etsy Ops | 0.1.0, enabled, baseline source tree | 0.1.0 enabled from older home-local tree | Drift |
| Working Modes | 0.1.0, enabled, baseline source tree | Not installed; home-local copy is only available and disabled | Drift |
| Motion Design Director | 0.1.0, enabled, baseline source tree | Not installed or available from a registered marketplace | Drift |
| Multi-Mailbox Ops | 0.1.0, enabled, MMO repository source | Exact version, enabled state, and source-tree digest | Pass |

The doctor's global-policy digest field currently uses the empty-tree digest because the helper traverses directory descendants while the policy is a file. This does not affect this apply result: an independent file SHA-256 comparison confirmed exact policy parity. No doctor code was changed in this phase.

## Read-only plugin inventory

Registered marketplace roots relevant to custom capability state:

- `home-local`: `/Users/maggielerman`
- `multi-mailbox-ops-local`: `/Users/maggielerman/Github/multi-mailbox-ops`
- `custom-plugin-backups`: not registered on the Air

The bundled, curated, and primary-runtime marketplaces were also present; they are outside this custom-plugin phase.

| Exact configured plugin ID | Configured enabled | Effective installed/available state | Observed source or expected baseline source |
|---|---:|---|---|
| `context-layer@home-local` | Yes | Installed and enabled, version 0.1.0 | Observed `/Users/maggielerman/plugins/context-layer`; baseline winner is this worktree's `plugins/context-layer` |
| `rps-etsy-ops@home-local` | Yes | Installed and enabled, version 0.1.0 | Observed `/Users/maggielerman/plugins/rps-etsy-ops`; baseline winner is this worktree's `plugins/rps-etsy-ops` |
| `working-modes@custom-plugin-backups` | Yes | Not installed; a 0.1.0 home-local copy is available but disabled | Expected baseline source: this worktree's `plugins/working-modes` |
| `motion-design-director@custom-plugin-backups` | Yes | Not installed and not available through a registered marketplace | Expected baseline source: this worktree's `plugins/motion-design-director` |
| `multi-mailbox-ops@multi-mailbox-ops-local` | Yes | Installed and enabled, version 0.1.0 | `/Users/maggielerman/Github/multi-mailbox-ops/plugins/multi-mailbox-ops` |

No plugin was added, removed, enabled, disabled, upgraded, or repointed in phase one. Plugin caches were inspected only as installation evidence and have no source precedence.

## Phase-two boundary

Before any plugin mutation, register the Git-backed `custom-plugin-backups` marketplace from this isolated worktree and prepare an explicit per-plugin apply/readback plan. Context Layer and RPS Etsy Ops must move from their older home-local sources to the baseline repository packages; Working Modes and Motion must be installed from the registered baseline marketplace. MMO already matches and should remain unchanged.
