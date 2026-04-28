# Codex Skills Audit Report

Audit date: April 19, 2026
Repository: `/Users/maggielerman/Github/codex-skills`

## Summary

| Check | Result | Notes |
| --- | --- | --- |
| Suite completeness | Pass | All 20 skills in `skills/SUITE_SKILLS.txt` exist in the repo and in local Codex state. |
| Main repo purpose | Clear | Curated portable skill suite plus selected custom plugin backups. |
| Biggest strengths | Strong | Docs/governance stack is coherent; execution stack is complementary; plugin backups are separated cleanly. |
| Biggest problems | Real | Portability drift, lifecycle metadata drift, duplicate tranche-orchestrator ownership, thin tests, generated junk files. |
| Best evaluator result | `design-system-refine` A/100 | Best overall target from Plugin Eval. |
| Most important action | Hardening | Fix portability and de-duplicate tranche orchestration before doing broader cleanup. |

## Suite Skills Table

| Skill | Cluster | Primary job | Works with | Lifecycle | Plugin Eval | Keep or absorb | Key issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ML-catalog-review` | Assessment | Shopify-first catalog review workflow and artifact loop | `ML-docs-system-scaffold` optional overlay | `active` | `C/72` | Keep separate | Large description; no helper tests |
| `ML-cluster-assignment` | Execution | Split work into safe parallel clusters and bootstrap worktrees | `ML-project-tranche-orchestrator` | `active` | `B/86` | Keep separate | Healthy overall; could add tests for shell helper |
| `ML-codex-to-claude-handoff` | Utilities | Generate Claude repo rules from Codex instructions | `ML-docs-system-scaffold` optional | `active` | `C/77` | Keep separate | Hard-coded paths; tests missing |
| `ML-collaborative-walkthrough` | Governance | Structured sign-off walkthrough for in-review projects | `ML-docs-system-scaffold`, `ML-project-tranche-orchestrator` | `active` | `B/86` | Keep separate | Low risk; mostly evaluator naming false positive |
| `ML-continue-until-blocked` | Execution | Continuous autonomous execution once scope is already approved | `ML-project-tranche-orchestrator` | `active` | `D/67` | Keep separate | Very long prompt; token heavy |
| `ML-docs-evidence-backfill` | Docs core | Retrofit fragmented evidence into canonical docs evidence system | `ML-docs-system-scaffold` | `active` | `C/72` | Keep separate | Portability links; trigger text is heavy |
| `ML-docs-product-pack` | Docs core | Deprecated shim pointing to scaffold flow | `ML-docs-system-scaffold` | `deprecated` | `C/81` | Absorb into scaffold | Deprecated shim only |
| `ML-docs-project-dashboard-legacy` | Docs core | Standalone retrofit for project dashboard output | `ML-docs-system-scaffold` | `active` in metadata, reads legacy in skill text | `D/63` | Absorb into scaffold | Metadata drift; should not still read as active |
| `ML-docs-project-lifecycle-statuses` | Docs core | Retrofit older repos with newer lifecycle states | `ML-docs-system-scaffold` | `legacy` | `D/68` | Keep legacy, then archive | Migration-only value |
| `ML-docs-system-scaffold` | Docs core | Create or standardize docs/governance/evidence system | evidence-backfill, walkthrough, tranche | `active` | `F/49` | Keep core | Portability issues; high token budget; dashboard path dependency |
| `ML-env-bootstrap-sync` | Utilities | Standardize env/bootstrap and worktree sync patterns | `ML-docs-system-scaffold` optional | `active` | `B/86` | Keep separate | Low risk; mostly evaluator naming false positive |
| `ML-github-docs-tracking-sync` | Utilities | Optional docs-to-GitHub tracking sync | `ML-docs-system-scaffold` optional | `active` | `D/63` | Maybe absorb later | Niche utility; helper complexity |
| `ML-hyphenomenon-project-intake` | Assessment | Create import-ready intake dossier plus screenshots | - | `active` | `D/68` | Keep separate | Helper tests missing |
| `ML-plan-signoff-review` | Governance | Final cross-check before plan approval | `ML-project-governance-audit` | `active` | `B/86` | Keep separate | Low risk; mostly evaluator naming false positive |
| `ML-project-governance-audit` | Governance | Audit roadmap order, blockers, and checkpoint hygiene | tranche, walkthrough, signoff | `active` | `C/81` | Keep separate | Description could be sharper |
| `ML-project-tranche-orchestrator` | Execution | Primary-agent tranche selection, delegation, review, and docs writeback | docs scaffold, continue, cluster | `active` | `F/54` | Keep, but de-dupe plugin | Duplicate with plugin; helper tests missing |
| `ML-repo-implementation-review` | Assessment | Compare 2-3 repos and generate report artifact | - | `active` | `F/54` | Keep separate | Large deferred bundle; helper complexity |
| `ML-shopify-app-scaffold` | Utilities | Scaffold Shopify app shell with reusable overlays | - | `active` | `D/63` | Keep separate | Hard-coded paths; helper complexity |
| `ML-user-journey-audit` | Assessment | Route and UX journey audit with PDF output | `ML-ux-ui-bug-intake` optional | `active` | `D/63` | Keep separate | Hard-coded paths; tests missing |
| `ML-ux-ui-bug-intake` | Utilities | Set up lightweight UX/UI bug intake workflow | `ML-user-journey-audit` optional | `active` | `C/77` | Keep separate | `openai.yaml` schema mismatch; hard-coded path |

## Plugin And Plugin-Skill Table

| Item | Type | Primary job | Works with | Plugin Eval | Keep or absorb | Key issues |
| --- | --- | --- | --- | --- | --- | --- |
| `design-system-first` | Plugin | Frontend starter and refinement bundle | `design-system-starter`, `design-system-refine` | `F/31` | Keep as plugin | Bundle score low because metadata and budget are heavy |
| `design-system-starter` | Plugin skill | Scaffold design-system-first Next.js starters | `design-system-refine` | `C/82` | Keep | Good candidate for test hardening |
| `design-system-refine` | Plugin skill | Refine an existing design-system-first starter | `design-system-starter` | `A/100` | Keep | Best evaluator result in audit |
| `project-tranche-orchestrator` | Plugin | Plugin packaging of tranche orchestration | suite tranche skill | `C/73` | De-dupe with suite skill | Should not be a second logic source |
| `project-tranche-orchestrator` | Plugin skill | Plugin-contained tranche orchestrator skill | suite `ML-project-tranche-orchestrator` | `C/81` | Absorb or sync | Use one canonical source |

## Cross-Cutting Findings

| Finding | Impact | Affects | Recommended action |
| --- | --- | --- | --- |
| Portability drift | High | `ML-docs-system-scaffold`, `ML-codex-to-claude-handoff`, `ML-user-journey-audit`, `ML-shopify-app-scaffold`, `ML-ux-ui-bug-intake`, and some docs links | Replace hard-coded `.codex` and user-specific paths with skill-relative guidance |
| Lifecycle metadata drift | High | `ML-docs-project-dashboard-legacy` | Mark as `deprecated` or `legacy` in `skills/SUITE_METADATA.json` and regenerate catalog |
| Duplicate source of truth | High | `ML-project-tranche-orchestrator` plus plugin copy | Choose one canonical source and sync or generate the other |
| Catalog parser mismatch | Medium | `ML-ux-ui-bug-intake` | Normalize `agents/openai.yaml` or extend `scripts/build_catalog.py` to support both metadata shapes |
| Generated junk in bundles | Medium | multiple skills/plugins | Remove `.DS_Store`, `__pycache__`, `.pyc`; update `.gitignore` |
| Thin test coverage | Medium | most helper-script skills | Add tests for tranche helpers, docs scaffold helpers, repo review helpers, and design-system starter |
| Default Plugin Eval rubric mismatch | Medium | almost all `ML-*` skills | Consider a custom metric pack so intentional `ML-*` naming stops dominating scores |

## Local Skills Not Mirrored In This Repo

| Status | Count | Notes |
| --- | --- | --- |
| Extra local skills not in repo allowlist | `26` | This is not a failure if the repo remains intentionally curated rather than a full mirror. |

| Local-only skills |
| --- |
| `atlas`, `cloudflare-deploy`, `codex-primary-runtime`, `doc`, `gh-address-comments`, `gh-fix-ci`, `imagegen`, `jupyter-notebook`, `netlify-deploy`, `notion-knowledge-capture`, `notion-meeting-intelligence`, `notion-research-documentation`, `notion-spec-to-implementation`, `openai-docs`, `pdf`, `playwright`, `playwright-interactive`, `render-deploy`, `screenshot`, `security-best-practices`, `sora`, `speech`, `spreadsheet`, `transcribe`, `vercel-deploy`, `wrapped` |

## Priority Actions

| Priority | Action | Why first |
| --- | --- | --- |
| 1 | Fix portability in flagship skills | Directly supports the repo's core promise that skills remain portable standalone bundles |
| 2 | De-dupe tranche orchestrator between suite and plugin | Prevents drift in one of the most important workflow skills |
| 3 | Correct lifecycle metadata for dashboard legacy skill | Makes generated catalog and repo status truthful again |
| 4 | Remove generated junk files | Quick cleanup that improves portability and professionalism |
| 5 | Add tests for highest-value helper scripts | Reduces regression risk in the most automation-heavy skills |
| 6 | Add custom Plugin Eval metric pack | Improves future audits by reducing low-signal naming penalties |
