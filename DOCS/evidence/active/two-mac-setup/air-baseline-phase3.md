# MacBook Air Baseline Apply — Phase 3

Recorded: 2026-09-01 05:11 ET (America/New_York)

## Scope and authorization

- Worktree: `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills`
- Branch: `codex/air-baseline-apply`
- Pre-change branch HEAD: `331d4125daa2a38588b6c2780c03710d80c8d416`
- Approved removals were limited to the obsolete registrations `context-layer@home-local` and `rps-etsy-ops@home-local`.
- The old source folders, home-local cache trees, prior workstation-bootstrap backups, migration/checkpoint branches, and all unrelated plugin state were preserved.

## Preservation method

The local plugin removal command was not used because its documented behavior removes both the config registration and its cache. Instead, each obsolete registration was removed by deleting only its exact two-line enabled section from the local Codex config after creating a recoverable config checkpoint. No other config field was changed during either removal.

Config checkpoints:

- Before Context Layer: `/Users/maggielerman/.codex/backups/workstation-bootstrap/20260901T090954Z-phase3-context/config.toml`
- Before RPS Etsy Ops, after Context Layer had passed: `/Users/maggielerman/.codex/backups/workstation-bootstrap/20260901T091041Z-phase3-rps/config.toml`

Each checkpoint's SHA-256 matched the live config immediately before its corresponding change. Raw config contents and values were not recorded in this evidence file.

Preserved old trees after completion:

| Preserved tree | Final digest |
|---|---|
| `/Users/maggielerman/plugins/context-layer` | `1b6c852f0ecbaf080c621abe5fb7d73b19e29ba3b8ad51e5abab14e390f56872` |
| `/Users/maggielerman/.codex/plugins/cache/home-local/context-layer/0.1.0` | `1b6c852f0ecbaf080c621abe5fb7d73b19e29ba3b8ad51e5abab14e390f56872` |
| `/Users/maggielerman/plugins/rps-etsy-ops` | `101c427f411299cef2fdc39b34ec5b2561016b86a23ad5a97edfed0c1e5bd8e3` |
| `/Users/maggielerman/.codex/plugins/cache/home-local/rps-etsy-ops/0.1.0` | `101c427f411299cef2fdc39b34ec5b2561016b86a23ad5a97edfed0c1e5bd8e3` |

## Context Layer reconciliation

Preconditions:

- `context-layer@home-local` was the only active Context Layer ID.
- `context-layer@custom-plugin-backups` 0.1.0 was available from the isolated Git-backed marketplace.
- Old source and cache digests both matched `1b6c852f...` before mutation.

Exact install command:

```text
codex plugin add context-layer@custom-plugin-backups --json
```

Result:

- Installed ID: `context-layer@custom-plugin-backups`
- Version: 0.1.0
- Enabled: yes
- Active source: `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills/plugins/context-layer`
- Source and installed-cache digest: `c8ff6322e383cf29d73b9126e938a066ae15c6794a1bf54887bcbe9dba6f9331`
- Obsolete `context-layer@home-local` ID: absent from installed config
- Former home source and cache: present and unchanged as inactive evidence

The intermediate doctor command was:

```text
python3 scripts/workstation_doctor.py --host-overlay config/host-overlay.local.json --json
```

It passed Context Layer, Working Modes, Motion Design Director, and Multi-Mailbox Ops. Its only remaining drift was RPS Etsy Ops, so the second reconciliation was allowed to proceed.

## RPS Etsy Ops reconciliation

Preconditions:

- `rps-etsy-ops@home-local` was the only active RPS Etsy Ops ID.
- `rps-etsy-ops@custom-plugin-backups` 0.1.0 was available from the isolated Git-backed marketplace.
- Old source and cache digests both matched `101c427f...` before mutation.

Exact install command:

```text
codex plugin add rps-etsy-ops@custom-plugin-backups --json
```

Result:

- Installed ID: `rps-etsy-ops@custom-plugin-backups`
- Version: 0.1.0
- Enabled: yes
- Active source: `/Users/maggielerman/Documents/Codex/2026-09-01/two-mac-baseline/codex-skills/plugins/rps-etsy-ops`
- Source and installed-cache digest: `e287f8b3da64fb7868b675d6be9bb493c2c4af7ab4b03f044d2cb72f3e00a4aa`
- Obsolete `rps-etsy-ops@home-local` ID: absent from installed config
- Former home source and cache: present and unchanged as inactive evidence

## Final effective plugin state

The only active custom IDs in this baseline set are:

| Active plugin ID | Version | Enabled | Active source |
|---|---:|---:|---|
| `context-layer@custom-plugin-backups` | 0.1.0 | Yes | Isolated baseline worktree `plugins/context-layer` |
| `rps-etsy-ops@custom-plugin-backups` | 0.1.0 | Yes | Isolated baseline worktree `plugins/rps-etsy-ops` |
| `working-modes@custom-plugin-backups` | 0.1.0 | Yes | Isolated baseline worktree `plugins/working-modes` |
| `motion-design-director@custom-plugin-backups` | 0.1.0 | Yes | Isolated baseline worktree `plugins/motion-design-director` |
| `multi-mailbox-ops@multi-mailbox-ops-local` | 0.1.0 | Yes | `/Users/maggielerman/Github/multi-mailbox-ops/plugins/multi-mailbox-ops` |

Working Modes, Motion Design Director, and Multi-Mailbox Ops were not changed during phase 3. The preserved home-local Context Layer and RPS packages remain visible only as disabled available candidates; they are not installed or active registrations.

## Final verification

Full tests:

```text
python3 -m unittest discover -s tests -p 'test_*.py'
```

Result: 17 tests passed, zero failures.

Final doctor:

```text
python3 scripts/workstation_doctor.py --host-overlay config/host-overlay.local.json --json
```

Result:

- Overall status: `pass`
- Checks: 18
- Non-passing checks: none
- Global policy and all 12 direct skills: pass
- All five required plugins: pass on ID-effective name, version, enabled state, and source digest
- Duplicate active Context Layer IDs: none
- Duplicate active RPS Etsy Ops IDs: none
- Remaining baseline drift: none

Plugin caches remain evidence only and are not source authority.
