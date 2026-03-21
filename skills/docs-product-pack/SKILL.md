---
name: docs-product-pack
description: Deprecated shim. Use `docs-system-scaffold` for product-doc scaffolding and docs governance/tooling in one workflow.
---

# Product Docs Pack (Deprecated)

This skill is deprecated and retained only for backward compatibility.

## New canonical path
Use `docs-system-scaffold` instead. It now includes product-doc pack scaffolding directly.

## Behavior
When this skill is requested:
1. Redirect to `docs-system-scaffold`.
2. Run in product-doc mode (`product docs pack: yes`).
3. Follow safe-write behavior (additive updates only; no file deletions).

## Why deprecated
- Avoid duplicated logic and drift between two docs-oriented skills.
- Keep one canonical skill for docs root, governance files, tooling, CI, and product docs.

## Legacy reference
Template reference remains here for compatibility:
- `references/product-doc-templates.md`
