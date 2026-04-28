# UX/UI Bug Intake Structure

Use this as the default lightweight structure for repositories that need a docs-backed UX/UI bug intake system without introducing per-bug files or a heavyweight issue tracker.

## Preferred Folder

- `DOCS/UX_UI_BUGS/README.md`
- `DOCS/UX_UI_BUGS/INBOX.md`
- `DOCS/UX_UI_BUGS/TRIAGED.md`
- `DOCS/UX_UI_BUGS/ARCHIVE.md`

If the repo uses `docs/`, keep the same folder name but mirror the repo's casing.

## Folder Roles

### `README.md`

Holds:

- entry schema
- severity/status vocabulary
- routing defaults
- fix-now vs defer rules
- subagent reporting contract
- operating rhythm

### `INBOX.md`

Use for:

- newly reported UX/UI bugs
- low-friction rough capture
- append-first logging before dedupe and normalization

### `TRIAGED.md`

Use for:

- normalized working queue
- owner stream assignment
- status after review
- planned or active tranche candidates

### `ARCHIVE.md`

Use for:

- `fixed`
- `wont-fix`
- `superseded`

## Default Entry Schema

- `ID`
- `Reported`
- `Detected by`
- `Actor`
- `Surface`
- `Summary`
- `Severity`
- `Status`
- `Likely owner`
- `Superseded by migration?`
- `Notes`

## Default Severity Vocabulary

- `blocker`
- `high`
- `medium`
- `low`

## Default Status Vocabulary

- `new`
- `triaged`
- `scheduled`
- `in active slice`
- `fixed`
- `wont-fix`
- `superseded`

## Canonical Operating Model

- user detects bugs
- main agent detects bugs
- subagents detect bugs
- main agent is the canonical logger/router

## Default Triage Rule

Fix immediately only when the issue:

- breaks a real workflow
- blocks verification or CI
- creates misleading workflow truth
- is tiny and local to the files already being edited
- is unlikely to be replaced by a near-term migration or redesign

Otherwise:

- capture it
- triage it
- pull it into the right planned tranche later
