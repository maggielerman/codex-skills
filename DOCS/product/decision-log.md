---
title: Decision Log
description: Product and docs decisions for Codex Skills Packs
status: stable
lastUpdated: "2026-04-28 12:04 ET (America/New_York)"
owner: Product
---

# Decision log

## 2026-04-28: Separate customer docs from repo maintenance docs

**Context:** The repo needs both internal operating memory and customer-facing documentation for purchasers.

**Decision:** Keep repo-native operating docs in `DOCS/` and the customer-facing marketing/implementation site in `docs-site/`.

**Tradeoffs:** Two documentation surfaces must stay aligned through generated catalog data and explicit docs workflows.

**Follow-ups:** Regenerate `DOCS/manifest.json`, `skills/manifest.json`, and `docs-site/src/lib/catalog.generated.ts` whenever suite metadata changes materially.
