---
name: design-system-refine
description: Refine an existing design-system-first starter by tightening tokens, hierarchy, component usage, copy density, and starter surfaces. Use when a generated starter feels too generic, uneven, visually noisy, or structurally inconsistent after the initial scaffold.
---

# Design System Refine

Use this skill after the initial scaffold exists and the next job is quality rather than creation.

Examples:
- “Tighten the tokens and make the surfaces feel more cohesive.”
- “Refine this app shell so it reads less like a starter.”
- “Standardize spacing, hierarchy, and shadcn usage.”
- “Make this marketing starter feel more premium without changing the stack.”

## Workflow

1. Inspect the starter before editing.
   - identify whether the weakest point is tokens, hierarchy, composition, density, motion, or copy
2. Preserve the starter's core contract.
   - keep the existing mode (`marketing-only` or `app-shell`)
   - keep the shared design-system foundation coherent
   - avoid rewriting into a different product shape unless the user asks
3. Refine in this order:
   - tokens and visual language
   - layout hierarchy and section jobs
   - shadcn composition and surface consistency
   - copy density and affordance clarity
4. Verify the resulting code still feels intentional on both desktop and mobile

## Companion Skills

Use adjacent skills when they sharpen the result:

- use `$frontend-skill` for art direction, hierarchy, and memorable motion
- use `$shadcn` when a refinement needs better component composition or registry-aware fixes
- use `$react-best-practices` when a cleanup changes component structure or performance-sensitive code

## Reference

Use `references/refinement-checklist.md` as the default review order so the refinement pass stays focused and doesn't devolve into random polishing.
