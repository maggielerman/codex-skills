# Codex Skills Library

This repository is the durable source of truth for Maggie Lerman's custom Codex skills library plus installable custom plugin packages.

The goals of this repo are simple:
- back up custom skills outside local Codex state
- package reusable skill groups as installable Codex plugins
- make the collection easier to browse, validate, and evolve
- share useful Codex workflow patterns publicly
- support Maggie Lerman's public work around practical human-agent workflows

## License

This repository is being prepared for public release, but a public license has not been selected yet.

Until an explicit license is added:
- all rights remain reserved by the repository owner
- any existing third-party or upstream license files preserved inside individual skill folders continue to apply to those specific files

## Repository layout

- `skills/` - the skill folders that belong to this curated suite
- `skills/SUITE_SKILLS.txt` - the allowlist of skill folders included in this repo
- `skills/SUITE_METADATA.json` - lifecycle metadata such as `active`, `legacy`, `deprecated`, or `archived`
- `skills/INDEX.md` - human-friendly catalog of the suite
- `skills/manifest.json` - machine-friendly metadata manifest
- `plugins/` - installable custom plugin packages
- `.agents/plugins/marketplace.json` - repo-local plugin marketplace for the packaged plugins
- `scripts/build_catalog.py` - validates suite drift, then regenerates the index and manifest from skill metadata
- `scripts/build_docs_site_catalog.py` - regenerates public docs-site catalog data from skill and plugin metadata
- `docs-site/` - Next.js/Tailwind/shadcn public marketing, catalog, and implementation docs site
- `DOCS/` - lean repo notes, project memory, and evidence that should remain useful in public
- `scripts/sync_from_codex_home.sh` - syncs local skills from Codex and agent skill homes into this repository
- `AGENTS.md` - operating instructions for agents working in this repo
- `CONTRIBUTING.md` - contribution and quality standards

## Working model

Each skill should remain self-contained and portable. The repo-level docs explain standards; the skill folders contain the actual behavior.

Custom plugins live under `plugins/` as installable packages. A plugin can bundle one or more skills, scripts, references, assets, or MCP/app configuration behind a single Codex install surface. Plugin metadata is indexed separately from the standalone skills catalog.

The repository intentionally tracks an allowlisted subset of local Codex skills rather than mirroring every installed skill. Plugin packages follow the same principle: only custom reusable plugins should be published here.

Use `skills/` for standalone skill source and public browsing. Use `plugins/` for grouped workflows that should be installed as a unit through the plugin marketplace.

Skill lifecycle state is tracked separately from membership:
- `active` means supported for normal use
- `experimental` means promising but still evolving; expect interface or behavior changes
- `legacy` means retained for narrow older scenarios
- `deprecated` means retained for backward compatibility and should point to a replacement
- `archived` means reference-only and should not be used for new work

The catalog files are generated from the skill folders. Before regeneration, the catalog script now checks for drift between `skills/`, `skills/SUITE_SKILLS.txt`, and `skills/SUITE_METADATA.json`. To audit without writing generated files, run:

```bash
python3 scripts/build_catalog.py --check
```

After adding or updating any skill, run:

```bash
python3 scripts/build_catalog.py
python3 scripts/build_docs_site_catalog.py
```

If you want to refresh the repo from local skill directories, run:

```bash
./scripts/sync_from_codex_home.sh --check
./scripts/sync_from_codex_home.sh --prune-stale
python3 scripts/build_catalog.py --check
python3 scripts/build_catalog.py
python3 scripts/build_docs_site_catalog.py
```

The sync preflight resolves allowlisted skills from `${CODEX_HOME:-$HOME/.codex}/skills` and `${AGENTS_HOME:-$HOME/.agents}/skills`. It reports allowlisted skills that are missing from local sources, local skills that are intentionally outside the curated suite, stale repo-only files inside synced skill folders, source-only files, and changed source files. Use `--prune-stale` in apply mode when the preflight identifies stale files that should be deleted from the repo copy.

If you update custom plugins, also refresh the repo-local plugin marketplace in `.agents/plugins/marketplace.json` so the package stays installable. Then run `python3 scripts/build_docs_site_catalog.py` so the public plugin docs stay current.

## Included skills

See [skills/INDEX.md](./skills/INDEX.md) for the current catalog.

## Public docs site

The `docs-site/` app is a Next.js, Tailwind, and shadcn site for sharing the skill catalog, plugin packages, and implementation notes publicly. Its pages should help readers understand, copy, adapt, and support the workflows. Do not use it for internal instructions about maintaining this repo.

The site catalog is generated from `skills/manifest.json` and custom plugin metadata. From the repo root, run:

```bash
python3 scripts/build_catalog.py
python3 scripts/build_docs_site_catalog.py
cd docs-site && npm run build
```

## Support

The current direction is public repo plus optional support. The docs site should make the work easy to evaluate and reuse, then route people to GitHub issues, contributions, stars, forks, and a support link when that destination is ready.
