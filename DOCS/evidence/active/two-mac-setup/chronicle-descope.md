---
title: Chronicle Visualizer Baseline De-scope
description: Records the removal of Chronicle Visualizer as a required two-workstation project while the Air shadow migration completes.
status: active
lastUpdated: 2026-09-01 06:34 ET (America/New_York)
owner: Engineering/Operations
---

# Chronicle Visualizer Baseline De-scope

## Decision

- Hyphenomenon owns current Skysight source durability, daily reporting,
  two-host aggregation, and publication contracts.
- Chronicle Visualizer remains a preserved historical experiment and immutable
  source-era record. It is not required on the Pro.
- The Air may retain its existing clone only until the Hyphenomenon-owned
  exact-day dry-run and non-uploading shadow cycle pass.
- The active Air durability automation remains unchanged until that evidence is
  recorded. The migration must repoint the single existing automation rather
  than create a duplicate writer.
- Existing encrypted objects, bucket paths, emergency archive data, passphrase,
  and historical Chronicle artifacts are preserved without migration or
  deletion.

## Baseline effect

- Removed `chronicle-visualizer` from required `projectRoles`.
- Removed its path from the host-overlay example.
- Added a non-binding transition record naming Hyphenomenon as the replacement
  and marking Chronicle as required on neither host.

## Remaining gate

The transition record can move to historical documentation after the Air proves
the exact Hyphenomenon commit, tool/key presence, old/new dry-run parity, one
complete non-uploading daily shadow cycle, and the first successful run after
repointing the existing automation.
