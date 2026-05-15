# GitHub Tracking Schema (1027 Transfer Baseline)

Use this baseline when transferring docs governance workflows into GitHub-native execution tracking.

## Source-of-Truth Split

- GitHub Issues/Projects: operational execution system (ownership, queue, triage, lifecycle).
- Docs (`DOCS/PROJECTS/*`, `ROADMAP.md`, `CHANGELOG.md`): governance system (policy decisions, checkpoints, release narrative).

## Single-Board Strategy

- Use one GitHub Project board for open execution work.
- Do not create one project board per docs file.

## Type Taxonomy

- `type:incident`
- `type:bug`
- `type:feature`
- `type:task`

## Priority Taxonomy

- `priority:p0`
- `priority:p1`
- `priority:p2`

## Area Taxonomy

- `area:seo-gates`
- `area:ops`
- `area:intake`
- `area:admin`
- `area:viz`
- `area:docs`

## Status Taxonomy

- `status:triaged`
- `status:in-progress`
- `status:blocked`
- `status:resolved`

## Environment Taxonomy

- `env:production`
- `env:preview`
- `env:local`

## Canonical Project Fields

- `Type` (`incident|bug|feature|task`)
- `Priority` (`p0|p1|p2`)
- `Area` (`seo-gates|ops|intake|admin|viz|docs`)
- `Docs Project ID` (text)
- `Incident ID` (text)
- `Start Date` (date)
- `Target Date` (date)
- `Completed Date` (date)
- Built-in `Status` (options normalized to `Inbox`, `Triaged`, `In Progress`, `Blocked`, `Done`)

## Recommended Views / Reporting

- `Execution Queue` (table)
- `Status Board` (board by status)
- `Feature Roadmap` (roadmap, `Type=feature`, date=`Target Date`)
- `Incident Triage` (table, `Type=incident`)
- Insights chart baseline: feature completion over time using `Completed Date`

## Docs-to-GitHub Mapping

- `project_id` -> issue body `Docs Project ID` + project field `Docs Project ID`
- `incident_id` -> issue body `Incident ID` + project field `Incident ID`
- docs status folder -> issue status label + project `Status` option
- docs checkpoints -> issue body `Next Checkpoint Target`
- roadmap execution order -> roadmap mirror issue checklist

## Marker Convention

Use hidden markers for idempotent upserts.

- Project issue marker: `<!-- docs-project-sync:key:project-<id> -->`
- Roadmap issue marker: `<!-- docs-project-sync:key:roadmap -->`

## Transfer Checklist

1. Verify docs discovery via `rg`.
2. Bootstrap labels.
3. Install issue templates.
4. Bootstrap/reuse single project board and fields.
5. Sync docs issues and roadmap issue.
6. Add items to board and map canonical fields.
7. Verify with `gh project item-list <n> --owner <owner> --format json`.
