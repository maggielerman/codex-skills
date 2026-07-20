---
name: hyphenomenon-codex-usage-report
description: Custom skill created by Maggie Lerman. Generate, analyze, validate, preview, and safely promote a Hyphenomenon Codex usage report. Use for daily or weekly Codex activity reports that require deterministic telemetry, GPT-5.6 Sol/high interpretation, Agent Stack evidence, Chronicle context, and fail-closed publication gates.
---

# Hyphenomenon Codex Usage Report

Custom skill created by Maggie Lerman.

Produce a period-specific Codex usage report while keeping deterministic evidence, interpretive analysis, preview, and publication permission separate.

## Runtime Contract

- Use GPT-5.6 Sol with high reasoning for every interpretive report run.
- If the model/reasoning configuration cannot be verified, stop before writing the analytical narrative and state the required configuration.
- Treat the Hyphenomenon repository's analyzer, validator, sync script, and report templates as the enforceable source of truth. Do not copy their logic into this skill.
- Generation is not permission to mutate production.

## Workflow

1. Orient in Hyphenomenon.
- Work from a clean, current Hyphenomenon checkout.
- Read `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`, and `DOCS/PROJECTS/active/1102_daily-codex-report-artifact-intake.md`.
- Confirm the requested start, end, timezone, report slug, title, publication visibility, and output run directory.
- Use explicit ISO boundaries in `America/New_York`; never infer a day from the current clock alone.

2. Generate deterministic evidence.

```bash
npm run intake:report:codex-usage -- \
  --start "<start-iso>" \
  --end "<end-iso>" \
  --timezone "America/New_York" \
  --slug "<report-slug>" \
  --title "<report-title>" \
  --summary "<baseline-summary>" \
  --project-slug "1102" \
  --output "DOCS/intake/runs/reports/<run>/artifact.json"
```

- Record the emitted analyzer version and source window.
- Require validation totals to reconcile before interpretation.
- Treat completed `mcp_tool_call_end` records as app/provider invocation evidence.
- Count a skill only when the operator explicitly requests it or a tool input observes a literal `SKILL.md` load. Do not count available tool/skill catalogs, and do not infer that a loaded skill was applied.

3. Perform the Sol/high analytical pass.
- Read the complete structured artifact before editing public prose.
- Identify the period's actual story: work blocks, repository distribution, verified delivery, output concentration, Agent Stack, Chronicle coverage, anomalies, and uncertainty.
- Lead with verified outcomes and meaningful patterns. Keep raw tool/event counts as supporting telemetry.
- Rewrite the title, summary, and sections for this period when the generated baseline is generic or misleading.
- Preserve deterministic numeric fields unless the analyzer is corrected and rerun.
- Never describe patch churn, commit-operation count, tool volume, app mentions, or Chronicle lane overlap as human productivity or duration.
- Keep analyzer-wide definitions in `Method Notes`; the template presents them in the metadata disclosure.

4. Validate and inspect data quality.

```bash
npm run intake:validate:report -- --artifact "DOCS/intake/runs/reports/<run>/artifact.json"
```

- Confirm every validation passes.
- Check that app/provider counts are completed invocations and skill rows carry `Requested`, `Loaded`, or both.
- Check repository labels, source links, summaries, and public prose for private paths, transcripts, IDs, secrets, or unsupported claims.
- If Chronicle coverage is partial, say so. Citation occurrences, unique cited minutes, and captured frames are different measures.

5. Preview without production mutation.
- For a public existing report, use only the guarded `.env.local` exact-target update path after a dry-run proves `nonDestructiveUpdate=true`.
- For a review-only report, use Hyphenomenon's development-only tracked review-artifact loader; do not sync it to the database.
- Review `/reports/<slug>` and `/evidence?type=report` at desktop/mobile widths, light/dark themes, keyboard navigation, and print layout.
- Require no runtime errors, console errors, horizontal overflow, or missing report/index links.

6. Gate publication.
- Commit and push the validated artifact, docs, and evidence on a review branch first.
- Production apply is allowed only when the active Hyphenomenon policy independently proves a clean `main`, a net-new target, schema-neutral additive behavior, no overwrite, a run-local rollback packet, successful production dry-run, route verification, and drift verification.
- Stop for existing targets, private/review-only visibility, schema changes, destructive behavior, ambiguous source coverage, or any failed validation.
- Never publish Chronicle review artifacts or source imagery through this skill without the separate approved Chronicle promotion plan.

## Completion Packet

Report:
- source window and timezone
- analyzer version
- Sol/high analytical story and material uncertainties
- artifact and local preview paths
- validation, test, build, and visual-QA results
- database target actually used, if any
- branch/PR status
- explicit statement of whether production or automation changed
