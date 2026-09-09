---
name: visual-design-critique
description: High-taste visual design, UI, and UX critique plus complete design audits for user-facing interfaces, screenshots, design concepts, prototypes, dashboards, apps, websites, landing pages, forms, design systems, and frontend implementations. Use when Codex is asked to do a design audit, complete design audit, UI audit, UX audit, visual audit, design-system audit, design critique, redesign, restyle, modernize, polish, compare visual options, audit screenshots/routes, assess sophistication or taste, verify implementation fidelity, or complete significant user-facing UI work before sign-off.
---

# Visual Design Critique

Custom local skill note: this is a Maggie-created custom skill, not a bundled default. Preserve this ownership note during future cleanup or migration so the skill does not get mistaken for generated scratch work.

Use this skill as a design-review gate, not as generic aesthetic encouragement. The job is to make UI work more intentional, legible, cohesive, and emotionally appropriate for its product context.

## Script paths

Run the `scripts/` commands below from this installed skill folder, using absolute paths for the target repository. Resolve the skill folder from its installed location; do not assume a particular username or checkout path.

## Start Here

1. Identify the mode: quick critique, implementation sign-off, complete design audit, concept comparison, design-system audit, or repair pass.
2. Identify the surface: product type, audience, primary job, platform, density needs, brand maturity, and whether this is a concept review, implementation review, or repair pass.
3. Gather evidence: screenshots, browser render, design concept, routes, existing design system, relevant code, user goals, constraints, and known acceptance criteria.
4. If reviewing implemented UI, inspect the real rendered surface. Use browser screenshots or supplied images rather than reasoning only from code.
5. If comparing many screens, variants, assets, or corrections, use `review-board-operating-pattern` for numbered visual packets, then apply this skill to the critique criteria.
6. If building a new frontend from scratch, pair with `frontend-app-builder`; this skill handles the taste gate, critique rubric, and final design-readiness judgment.

## Critique Lenses

Evaluate the interface through these lenses, in this order:

1. Product intent: the first read communicates what the product is, who it is for, and what action matters.
2. Information architecture: hierarchy, grouping, labels, navigation, and progressive disclosure match the user's mental model.
3. Composition: alignment, grid, balance, density, whitespace, edge behavior, and first-viewport framing feel deliberate.
4. Typography: scale, weight, line height, measure, control text, data labels, and responsive wrapping are legible and polished.
5. Color and material: palette, contrast, status colors, surfaces, shadows, depth, and emphasis are coherent and not decorative noise.
6. Component quality: buttons, forms, tables, cards, tabs, icons, charts, modals, empty states, and navigation have consistent anatomy and states.
7. Interaction clarity: controls reveal affordance, feedback, loading, errors, undo/escape paths, focus, selected states, and completion states.
8. Accessibility and resilience: contrast, target size, focus visibility, keyboard paths, reduced-motion needs, mobile layout, and overflow are checked.
9. Taste and restraint: every visual choice earns its place; decorative devices support meaning, brand, or hierarchy instead of filling space.

## Hard Stops

Do not call a UI/design pass complete while any of these remain fixable:

- unreadable text, weak contrast, tiny control labels, clipped content, or mobile overflow
- unclear primary action, weak first read, or hierarchy that makes users hunt for the main task
- generic template feel, mismatched brand tone, one-note palette, decorative clutter, or repeated filler cards
- inconsistent spacing, radii, borders, shadows, icon styles, type sizes, or component states
- inert controls, missing loading/error/empty states, invisible focus, no escape path, or ambiguous destructive actions
- screenshots that visibly drift from an accepted concept without an explicit approved deviation

## Output Standard

Lead with judgment before details:

- Verdict: ready, close with fixes, or not ready.
- Top issues: ordered by user impact and visual severity.
- Evidence: cite screenshot regions, routes, components, or file paths.
- Fix direction: concrete changes to layout, type, color, copy, component anatomy, states, or interaction flow.
- Verification plan: what must be re-screenshotted or retested before sign-off.

Prefer direct, specific critique over vague language like "make it cleaner" or "more modern." Say what to remove, resize, align, demote, emphasize, simplify, or verify.

## Complete Design Audit Mode

Use this mode when the user asks for a design audit, complete design audit, UI/UX audit, visual audit, product experience audit, design-system audit, or broad route/screenshot audit.

1. Define the audit scope: routes/screens, viewports, key flows, user roles, states, devices, known problem areas, and excluded surfaces.
2. Build an evidence inventory: screenshots, routes, source components, design-system docs, analytics or user feedback if available, and existing bug/design registers.
3. Audit representative states, not just happy paths: empty, loading, error, success, disabled, selected, hover/focus, mobile, dense data, long copy, and permission-restricted views.
4. Separate findings into:
   - screen-level issues
   - flow-level issues
   - design-system/component issues
   - accessibility/responsive issues
   - brand/taste/cohesion issues
   - content/labeling issues
5. Score every finding as `Must fix`, `Should fix`, or `Polish`, and identify whether it is local, repeated, or systemic.
6. Prioritize remediation by user harm and leverage: fix systemic tokens/components before one-off screen polish when that will remove repeated defects.
7. Produce an audit report with an executive verdict, evidence index, issue table, systemic themes, quick wins, deeper redesign candidates, and verification plan.
8. If the repo has an OS scaffold, create or update a numbered project doc and store durable evidence under the repo evidence system only when it will be useful for follow-up.

For large audits, use numbered review boards so feedback can refer to specific screens or regions without ambiguity.

## Repo OS Hooks

When a repository has a product operating system:

- Add visual/UX success criteria to the project doc for any user-facing UI stream.
- Record critique checkpoints before moving a project to `in-review`.
- Store screenshots, review-board packets, or audit artifacts under the repo's evidence system when they are intentionally preserved.
- Convert discovered defects into the repo's UX/UI bug intake if one exists.
- Use `MAGGIE TODO:` when human taste approval, manual screenshot review, or external brand input gates completion.

## Backfill Existing Scaffolded Repos

For repos that already have the product operating system scaffold but predate this skill, run:

```bash
python3 scripts/backfill_visual_design_gate.py --repo /path/to/repo
```

Use `--dry-run` first when you want a change preview. The script detects `DOCS/`, `docs/`, or `documentation/`; requires a `PROJECTS/` system; creates the visual design quality guide; and safely appends missing references to `AGENTS.md`, docs indexes, the projects index, and the active project template.

## References

Read `references/critique-rubric.md` when a fuller rubric, source-backed rationale, or OS integration language is needed.
