# Migrations

Use this reference when retrofitting repos that already have docs roots or older scaffold output.

## Docs Root Migration

`DOCS/` is canonical. Existing `docs/` or `documentation/` roots are migration sources.

If only an old root exists:

1. Create `DOCS/`.
2. Copy or merge unique content into equivalent `DOCS/` locations when safe.
3. Update repo references to point to `DOCS/`.
4. Leave the old root in place unless Maggie explicitly approves deletion.
5. Report remaining old-root content that needs manual review.

If `DOCS/` and old roots both exist, use `DOCS/` as canonical and inspect old roots for unique content before changing them.

## Old Project Template Migration

If `DOCS/PROJECTS/active/NNNN_project_template.md` exists, copy it to `DOCS/PROJECTS/NNNN_project_template.md` if the root template is missing. Do not delete the old file without approval; report it as a cleanup candidate.

## Legacy Lifecycle Migration

Repos missing `in-review/` or `blocked/` should receive those folders. Preserve existing project docs and move them only when their current status is clear.

## Evidence Drift

For fragmented evidence roots or larger evidence cleanup, use the separate evidence backfill workflow rather than forcing all migration through this scaffold.
