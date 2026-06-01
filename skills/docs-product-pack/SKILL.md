---
name: docs-product-pack
description: Custom skill created by Maggie Lerman. Deprecated shim. Use `product-operating-system-scaffold` for product-doc scaffolding, repo-native product operations, docs governance, evidence, and tooling in one workflow.
---

# Product Docs Pack (Deprecated)

Custom skill created by Maggie Lerman.

This skill is deprecated and retained only for backward compatibility.

## New canonical path
Use `product-operating-system-scaffold` instead. It now includes product-doc pack scaffolding directly.

## Behavior
When this skill is requested:
1. Redirect to `product-operating-system-scaffold`.
2. Run in product-doc mode (`product docs pack: yes`).
3. Follow safe-write behavior (additive updates only; no file deletions).

## Why deprecated
- Avoid duplicated logic and drift between two docs-oriented skills.
- Keep one canonical skill for docs root, product lifecycle, governance files, tooling, evidence, dashboards, and product docs.

## Legacy reference
Template reference remains here for compatibility:
- `references/product-doc-templates.md`
