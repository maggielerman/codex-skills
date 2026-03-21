# Repository Guidance

This repository stores portable custom Codex skills and the docs/scripts that maintain the suite.

## Operating assumptions

- Treat `skills/` as the primary product.
- Treat `skills/SUITE_SKILLS.txt` as the source of truth for which skills belong in this repo.
- Treat `skills/SUITE_METADATA.json` as the source of truth for lifecycle labeling such as `experimental`, `legacy`, `deprecated`, and `archived`.
- Keep the repository lean; avoid project-management scaffolding that is meant for delivery repos.
- Preserve portability. A skill copied out of this repo should still work as a standalone skill.
- Prefer repo-wide conventions over one-off formatting changes.

## Required workflow

When adding or updating skills:
- keep each skill folder self-contained
- preserve existing bundled licenses or notices found inside imported skills
- do not remove provenance-sensitive files unless explicitly asked
- update `skills/SUITE_SKILLS.txt` when adding or removing a suite skill
- update `skills/SUITE_METADATA.json` when a skill's lifecycle status changes
- regenerate `skills/manifest.json` and `skills/INDEX.md` with `python3 scripts/build_catalog.py`
- update top-level docs when the repo structure or contribution process changes materially

## Scope boundaries

- Do not add a public open-source license unless the user explicitly requests one.
- Do not import hidden/system skills such as `.system/` unless explicitly requested.
- Do not mirror every installed local skill into this repo; only track allowlisted suite skills.
- Do not silently rewrite imported skills just to normalize tone or structure; preserve intent unless there is a clear repo-wide reason to refactor.

## Quality bar

- Skill metadata must stay trigger-oriented and accurate.
- Experimental, deprecated, legacy, and archived skills must be visibly labeled in repo-level metadata and generated catalog output.
- Public-facing docs should be clear enough for future external sharing.
- Scripts should use the standard library when practical and avoid unnecessary dependencies.
