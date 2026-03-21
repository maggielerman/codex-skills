# Contributing

This repository is a curated skills library. Contributions should improve portability, clarity, and repeatable reuse.

## What belongs here

Good additions include:
- new Codex skills with clear triggering behavior
- improvements to existing skill instructions
- reusable scripts, references, or assets that materially strengthen a skill
- catalog, validation, and sync tooling for the repo itself

Avoid adding:
- repo-specific project management docs
- one-off experiment artifacts
- large reference dumps that are not directly used by a skill
- redundant documentation that restates what already exists in `SKILL.md`

## Skill standards

Each skill should:
- live in its own folder under `skills/`
- be listed in `skills/SUITE_SKILLS.txt`
- have an accurate lifecycle entry in `skills/SUITE_METADATA.json`
- include a valid `SKILL.md`
- use concise, trigger-oriented frontmatter
- include only the resource folders it actually needs
- remain portable outside this repo

When relevant, preserve:
- `agents/openai.yaml`
- bundled scripts
- bundled references
- bundled assets
- upstream license or notice files that already ship with the skill

## Naming and writing guidelines

- Use lowercase hyphen-case folder names.
- Keep descriptions explicit about when the skill should be used.
- Prefer short, high-signal instructions over long conceptual explanations.
- Design for another Codex instance that needs procedural guidance, not marketing copy.

## Before opening a change

1. Add or update the skill files.
2. Update `skills/SUITE_SKILLS.txt` if the suite membership changed.
3. Update `skills/SUITE_METADATA.json` if the skill is `experimental`, `legacy`, `deprecated`, or `archived`, and include a replacement or note when applicable.
4. Regenerate the catalog:

```bash
python3 scripts/build_catalog.py
```

5. Review the generated diff for `skills/INDEX.md` and `skills/manifest.json`.
6. Sanity-check that the repo docs still describe the repo accurately.

## Licensing note

This repository is intended for a future paid-access distribution model.

Until a formal commercial license is added:
- treat the repository as all rights reserved
- do not assume contribution implies open-source licensing
- do not add or change top-level licensing terms without explicit owner direction
