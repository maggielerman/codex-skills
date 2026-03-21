# Codex Skills Suite

This repository is the durable source of truth for the custom Codex skills suite: a curated library of authored skills, prompts, scripts, references, and assets that extend Codex for repeated workflows.

The goals of this repo are simple:
- back up the custom skills outside local Codex state
- make the collection easier to browse, validate, and evolve
- support a future paid distribution model for the full suite
- keep the catalog public-ready even while licensing and packaging decisions are still evolving

## Current licensing posture

This repository is not open source today.

Until a formal commercial license is added:
- all rights remain reserved by the repository owner
- access to the repository does not grant redistribution, resale, sublicensing, or public republishing rights
- any existing third-party or upstream license files preserved inside individual skill folders continue to apply to those specific files

When the paid-access model is finalized, this repository should add a dedicated commercial license or terms document that defines subscriber rights clearly.

## Repository layout

- `skills/` - the skill folders that belong to this curated suite
- `skills/SUITE_SKILLS.txt` - the allowlist of skill folders included in this repo
- `skills/INDEX.md` - human-friendly catalog of the suite
- `skills/manifest.json` - machine-friendly metadata manifest
- `scripts/build_catalog.py` - regenerates the index and manifest from skill metadata
- `scripts/sync_from_codex_home.sh` - syncs local Codex skills into this repository
- `AGENTS.md` - operating instructions for agents working in this repo
- `CONTRIBUTING.md` - contribution and quality standards

## Working model

Each skill should remain self-contained and portable. The repo-level docs explain standards; the skill folders contain the actual behavior.

The repository intentionally tracks an allowlisted subset of local Codex skills rather than mirroring every installed skill.

The catalog files are generated from the skill folders. After adding or updating any skill, run:

```bash
python3 scripts/build_catalog.py
```

If you want to refresh the repo from the local Codex skills directory, run:

```bash
./scripts/sync_from_codex_home.sh
python3 scripts/build_catalog.py
```

## Included skills

See [skills/INDEX.md](/Users/maggielerman/Github/codex-skills/skills/INDEX.md) for the current catalog.

## Future commercialization direction

The likely end state is a proprietary commercial license for the full suite. In practice, that usually means:
- customers pay for access to the bundle
- customers receive a limited license to use the skills
- redistribution, repackaging, and resale remain prohibited unless explicitly authorized
- updates and support can be tied to an active subscription or purchase tier

That model fits this repository better than an open-source license.
