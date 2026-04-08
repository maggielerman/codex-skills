---
name: user-journey-audit
description: Create current-state user journey audits with route mapping, screenshots, coverage verification, and a final PDF report. Use when Codex needs to audit navigation or UX flows for one or more user types in any repository or deployed app, suggest which user types to include, capture click-by-click evidence, verify route coverage against code and tests, and export a screenshot-backed PDF artifact.
---

# User Journey Audit

## Overview

Audit current-state navigation for one or more user types, preserve the evidence in docs, and export a final PDF report that combines diagrams, tables, screenshots, and coverage verification.

Keep the work current-state only unless the user explicitly asks for synthesis or redesign later.

## Workflow

1. Determine the audit source.
   - Prefer the live or production deployment when it exists and is accessible.
   - Use the local app or repo routes and tests as secondary evidence for route coverage.
   - State which source is primary before capturing.

2. Determine which user types to include.
   - If the user already named them, use that list.
   - If not, inspect sidebar labels, auth/demo fixtures, seed data, route families, and E2E tests to suggest likely user types.
   - Load [references/user-type-discovery.md](references/user-type-discovery.md) when you need a repo-agnostic method for suggesting which user types to include.
   - Ask the user to confirm the included user types only when they have not already specified them.
   - Support one user type or multiple user types; do not assume there must be three.

3. Create a stable audit output location.
   - Prefer `<repo>/DOCS/JOURNEY_AUDIT/` when `DOCS/` exists.
   - Otherwise prefer `<repo>/docs/journey-audit/`.
   - Otherwise fall back to `<repo>/output/journey-audit/`.
   - Keep screenshots inside a `screenshots/` subtree.
   - Keep the final PDF inside the audit docs folder as well as any secondary `output/pdf/` copy the repo already uses.

4. Capture the current-state walkthrough for each user type.
   - Start from the actual entry surface for that user type.
   - Traverse sidebar or top-level nav first.
   - Traverse dashboard cards, shortcuts, tabs, filters, query-state workspaces, detail views, and modal or sheet states that create distinct decisions.
   - Record exact click labels, origin screen, destination route or state, and screenshot path for every landed screen.
   - Treat query-state workspaces as distinct when they materially change the visible workspace.

5. Verify coverage before claiming completeness.
   - Inventory route files and navigation entrypoints from the codebase.
   - Check tests for hidden query-state paths, aliases, token routes, and handoff flows.
   - Produce an explicit coverage verification section.
   - Do not claim full coverage if the audit only covers primary flows.

6. Produce the audit artifacts.
   - Create a wrapper doc for shared findings.
   - Create one role doc per included user type.
   - Build a PDF report from a manifest using `scripts/render_journey_audit_pdf.mjs`.
   - Use the PDF as the easiest review artifact, but keep the source docs and screenshots beside it.

7. Validate the PDF visually.
   - Render PDF pages to PNG with `pdftoppm`.
   - Check that tables fit, diagrams render, screenshots are readable, and page breaks are sane.
   - Fix layout problems before delivering.

## Output Requirements

- Stay literal about current-state routes, labels, screenshots, and trust issues.
- Include role-aware matrices. If a table compares redundancy or terminology, identify the user type explicitly by row.
- Keep cross-role route reuse color-coded by user type in the PDF.
- Add a coverage-verification section whenever the user asks for “all routes,” “all paths,” or “entire journey.”
- Store the final PDF in the audit docs folder so it is not easy to lose.

## Suggested Audit Structure

Load [references/report-schema.md](references/report-schema.md) before building the manifest.
Load [references/invocation-recipe.md](references/invocation-recipe.md) when you want a ready-to-use prompt pattern for a fresh repo.

Use the scaffold script to initialize a manifest quickly:

```bash
python3 /Users/maggielerman/.codex/skills/user-journey-audit/scripts/init_journey_audit_manifest.py \
  --title "Project Journey Audit" \
  --audit-root /absolute/path/to/DOCS/JOURNEY_AUDIT \
  --output /absolute/path/to/journey-audit-manifest.json \
  --role family:Family \
  --role donor:Donor
```

Recommended artifacts:
- `README.md` or wrapper audit doc
- one role doc per user type
- `coverage-verification.md`
- `screenshots/<role>/...`
- `<audit-root>/<stable-report-name>.pdf`

## Coverage Checklist

Load [references/coverage-checklist.md](references/coverage-checklist.md) when verifying whether the audit really covers the current route graph.

Use it to check:
- query-state workspaces
- aliases and redirects
- tokenized invite/share/public routes
- list filters
- selected-item workspace states
- dashboard shortcuts that land on non-sidebar routes

## PDF Renderer

Use the bundled renderer when you want the same final report style across repositories:

```bash
node /Users/maggielerman/.codex/skills/user-journey-audit/scripts/render_journey_audit_pdf.mjs \
  --input /absolute/path/to/journey-audit-manifest.json \
  --output /absolute/path/to/final-report.pdf
```

The renderer expects a JSON manifest. The required shape and field meanings are documented in [references/report-schema.md](references/report-schema.md).

## User-Type Suggestion Pattern

When the user did not give you a final role list, suggest likely user types in this order:
- roles implied by auth and seed/demo fixtures
- roles implied by sidebar navigation shells
- roles implied by route families and E2E fixtures

Then ask for confirmation in one short question. Suggest 1-5 user types, not an open-ended taxonomy.

## Important Guardrails

- Avoid future-state synthesis until the user asks for it after the audit.
- Avoid claiming “complete” coverage unless the coverage verification section supports that claim.
- Prefer live evidence over inferred behavior when the app is accessible.
- When auth or data access is limited, state exactly which parts were directly observed versus inferred from code or tests.
