---
title: Docs library refresh
description: A searchable documentation library with clearer navigation and source access.
status: in-review
lastUpdated: "2026-09-09 13:40 ET (America/New_York)"
owner: Maggie Lerman
---

# Docs library refresh

The public site now uses a persistent documentation sidebar, restrained typography, and a searchable library instead of a long marketing page. Context Layer is the featured starting point. Existing skill and plugin URLs remain available.

## Changes

- Search matches names, descriptions, and categories; type filters show all items, skills, or plugins. Empty states offer a filter reset.
- A getting-started page explains skill versus plugin packaging, current license boundaries, and a concrete first task.
- Detail pages link to the actual bundled skills or reference guides and the full source folder.
- Mobile navigation remains visible and the library reflows into readable rows.
- The catalog parser now reads literal and folded multiline descriptions, fixing the visible `|` and `>` placeholders for Chronicle and Shopify merchant onboarding.

## Validation

- Repository tests: 12 passed, including multiline-description regression coverage.
- Suite drift check, documentation links, docs lint, and static production build passed (72 routes).
- Browser checks covered search results, no results/reset, seven-plugin filtering, Context Layer's included source links, and a 390px mobile viewport with no horizontal overflow.
- Desktop and mobile screenshots were reviewed against the generated visual direction. The implementation keeps the repository's real catalog content and directory structure.

The implementation is ready for visual feedback. Public access does not grant an open-source license; existing license and attribution boundaries are retained.
