---
title: Changelog
description: Chronological list of notable changes
status: stable
lastUpdated: "2026-07-20 09:56 ET (America/New_York)"
owner: Engineering
---

# Changelog

All notable changes to this project will be documented in this file.

<!-- NEW CHANGELOG ENTRIES START BELOW -->

### **2026-07-20 09:56 ET (America/New_York) - Hyphenomenon Codex usage report skill**
- Added project `1102` and the `hyphenomenon-codex-usage-report` skill with deterministic analyzer delegation, GPT-5.6 Sol/high interpretation, evidence-level checks, local preview, and fail-closed publication gates.
- Regenerated the suite/public catalogs and moved the skill project to in-review after catalog drift, docs-site lint/build, and link checks passed.

### **2026-04-28 12:04 ET (America/New_York) - Initial Setup**
- Established repo-native product operating system

### Entry Format Guidance
- Include project reference when available (example: `[1005]`).
- Generate timestamps with `node scripts/docs/timestamp-et.mjs --json` (never hand-type them).
- Prefer checkpoint-style summaries:
  - what was completed
  - what changed
  - what is next
