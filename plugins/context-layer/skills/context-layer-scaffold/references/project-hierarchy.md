# Project Hierarchy

Use this reference to create consistent parent projects, subprojects, and supporting project docs.

## When To Create A Parent Project

Use a parent project when the work is broad enough to contain multiple independently trackable streams. Good signals:

- multiple deliverables with different completion states
- separate owners or review paths
- child streams that may be blocked while other work continues
- separate evidence or verification packets
- a program/initiative that needs dashboard rollup

Set frontmatter:

```yaml
projectType: parent
programTrack: <track-name>
parentProject:
```

## When To Create A Subproject

Create a subproject when a unit of work has distinct scope, lifecycle state, risks, evidence, or sign-off. Do not create a subproject for a minor checklist item that belongs in the parent checkpoint log.

Subprojects move through lifecycle folders independently. A parent may remain active or in-review while child projects are blocked, completed, or active; record the rollup state in the parent checkpoint log.

Set frontmatter:

```yaml
projectType: child
parentProject: "1001_parent_slug"
programTrack: <track-name>
```

## Numbering

Use independent numeric prefixes for both parent projects and subprojects:

- `1001_parent_program.md`
- `1002_child_stream.md`
- `1003_second_child_stream.md`

Use `parentProject` frontmatter for hierarchy instead of hierarchical filenames. This keeps lifecycle movement simple and avoids filename parsing ambiguity.

## Supporting Docs And Evidence

Keep `DOCS/PROJECTS/` for lifecycle project docs plus the root template. Store durable supporting artifacts under evidence:

- `DOCS/evidence/active/<project-id>/`
- `DOCS/evidence/archive/<project-id>/`
- `DOCS/evidence/active/<project-id>/review-packets/<run-name>/`

Short notes, decisions, and rollups belong in the project doc. Larger audits, screenshots, manifests, CSVs, PDFs, or review packets belong in evidence and should be linked from the project doc.

## Dashboard Expectations

The dashboard should group child streams by `parentProject` and `programTrack`, surface blocked or in-review child streams, and flag orphaned child projects whose parent cannot be found.
