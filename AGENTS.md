# Repository Guidance

This repository stores portable Codex skills and the docs/scripts that maintain the suite.

## Operating assumptions

- Treat `skills/` as the primary product.
- Keep the repository lean; avoid project-management scaffolding that is meant for delivery repos.
- Preserve portability. A skill copied out of this repo should still work as a standalone skill.
- Prefer repo-wide conventions over one-off formatting changes.

## Required workflow

When adding or updating skills:
- keep each skill folder self-contained
- preserve existing bundled licenses or notices found inside imported skills
- do not remove provenance-sensitive files unless explicitly asked
- regenerate `skills/manifest.json` and `skills/INDEX.md` with `python3 scripts/build_catalog.py`
- update top-level docs when the repo structure or contribution process changes materially

## Scope boundaries

- Do not add a public open-source license unless the user explicitly requests one.
- Do not import hidden/system skills such as `.system/` unless explicitly requested.
- Do not silently rewrite imported skills just to normalize tone or structure; preserve intent unless there is a clear repo-wide reason to refactor.

## Quality bar

- Skill metadata must stay trigger-oriented and accurate.
- Public-facing docs should be clear enough for future external sharing.
- Scripts should use the standard library when practical and avoid unnecessary dependencies.
