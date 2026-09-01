# MacBook Air Skill and Plugin Parity Audit

Audit date: 2026-09-01
Scope: read-only capability inventory completed before this evidence record was written. Plugin caches are installation evidence only and are never source authority.

## Repository anchors

- `codex-skills` Air branch: `codex/migration-air-state-20260831`
- Air HEAD: `7dc67f55cf3afa47f162eebad72c8336a9476ce0`
- Confirmed `origin/main`: `d8f26f5bf5eb9272b7a1d9dac981aa02891aca26`
- Relationship at audit time: Air was one commit ahead and two commits behind `origin/main`.
- `multi-mailbox-ops` Air branch: `codex/migration-air-state-20260831`
- MMO Air HEAD: `39db2f161194edd37a0dbf26df3ef63e696da789`
- MMO `origin/main`: `b5eef18624ca89dbd8b4d7ffc009f9d1634eee03`
- Relationship at audit time: MMO Air was one commit ahead of `origin/main`.

## Direct skill inventory

There were 68 first-level direct skills under `~/.codex/skills`, excluding the system-managed `.system` directory. The current Air branch tracked 56 suite skills; `origin/main` tracked 57.

Direct skills absent from the current Air branch's `skills/SUITE_SKILLS.txt`:

`artifact-template-rps-8x10-gallery-sleeve-package`, `autonomous-backlog-runner`, `autonomous-backlog-scaffold`, `cloudflare-deploy`, `codex-primary-runtime`, `gh-address-comments`, `gh-fix-ci`, `hyphenomenon-codex-usage-report`, `imagegen`, `jupyter-notebook`, `netlify-deploy`, `notion-knowledge-capture`, `notion-meeting-intelligence`, `notion-research-documentation`, `notion-spec-to-implementation`, `openai-docs`, `pdf`, `playwright`, `playwright-interactive`, `remote-image-visual-review`, `render-deploy`, `rps-print-order`, `screenshot`, `security-best-practices`, `sora`, `speech`, `tmora-postcard-production`, `tmora-shopify-product-intake`, `transcribe`, `vercel-deploy`, `wrapped`.

Against `origin/main`, remove `hyphenomenon-codex-usage-report` from that list. The direct Air copy of that skill matched the `origin/main` version file-for-file.

Suite skills absent from `~/.codex/skills`:

`chronicle`, `shopify-admin`, `shopify-admin-execution`, `shopify-custom-data`, `shopify-customer`, `shopify-dev`, `shopify-functions`, `shopify-hydrogen`, `shopify-liquid`, `shopify-merchant-onboarding`, `shopify-onboarding-dev`, `shopify-partner`, `shopify-payments-apps`, `shopify-polaris-admin-extensions`, `shopify-polaris-app-home`, `shopify-polaris-checkout-extensions`, `shopify-polaris-customer-account-extensions`, `shopify-pos-ui`, `shopify-storefront-graphql`.

All 18 Shopify skills were present under `~/.agents/skills`; this was a location discrepancy rather than missing capability. `chronicle` was not found in either direct-skill location.

## Enabled custom plugins and sources

| Plugin | Version | Enabled source | Audit result |
|---|---:|---|---|
| Context Layer | 0.1.0 | `/Users/maggielerman/plugins/context-layer` | Cache matched the home source; the repository copy under `plugins/context-layer` was newer and different. |
| RPS Etsy Ops | 0.1.0 | `/Users/maggielerman/plugins/rps-etsy-ops` | Cache matched the home source; the repository copy under `plugins/rps-etsy-ops` differed. |
| Working Modes | 0.1.0 | `custom-plugin-backups` source registration unresolved | Cache matched `plugins/working-modes`; the separate home copy differed. |
| Motion Design Director | 0.1.0 | `custom-plugin-backups` source registration unresolved | Cache matched `plugins/motion-design-director`. |
| Multi-Mailbox Ops | 0.1.0 | `/Users/maggielerman/Github/multi-mailbox-ops/plugins/multi-mailbox-ops` | Source and cache matched exactly. |

Design System First 0.1.0 was installed but disabled. Jamstack Expert 0.2.0 and Project Tranche Orchestrator 0.1.0 had local source entries but were not enabled as plugins; their direct skills supplied the active capability.

## Complete-directory SHA-256 differences

The audit's directory hash used sorted paths, file type, mode, symlink target, and file-content SHA-256.

| Skill | Repository | Direct Air copy | Assessment |
|---|---|---|---|
| `catalog-review` | `32d0c08034e3c5fccc405a839fc122be7363afbc2cc76af323ce7e116a787c5c` | `6886a031b106b04e1a1e5ad3f4a820f432f8613c6585fbe645002a8e204a0ff1` | Air copy was newer by file history. |
| `hyphenomenon-chat-intake` | `2466261b5e93e6365eb5a5cc526dfb524471c7d71556ca58e742cd1332766d06` | `d9cd0f6b972e2cc6d0dfb6f8272860f8e764abba8363556268e2c71339c2a272` | Air copy used the forward `DOCS/intake` path; chronology was inconclusive. |
| `hyphenomenon-project-intake` | `210ba133ea6775f5887d75c8876c17dee9cbbc759a982b473109d928e634bbdb` | `fcd63d920591d639396c2b2fc7c9e9fa92604d473c91cd52b09ab0b82b195ff2` | Air copy used the forward Hyphenomenon-owned intake layout; chronology was inconclusive. |
| `tmora-print-proof-deck` | `f70c82f07e8e64309f82fd7f0871195ce18430062c2be72897c6e76b51fe6cb8` | `1ddfe39e7a3cc3001732d13f96dd61510a225eed3bc17aea9426cfaf19a90d4c` | Air copy was materially newer. |
| `visual-design-critique` | `cf13b14540cdb3a411a861724a27d2d3a94b3efe2939f775c4cb976bf07b56ef` | `cd6a2c4ef794fcd0a28498e79386769d763b7ddeb211562ac112bd02434749b1` | Substantive files matched; difference was generated `__pycache__` only. |

## Capability verdicts

- **Context Layer:** functional. The active bundle contained ten skills, but omitted `context-layer-dashboard-backfill` and carried an older `context-layer-scaffold`. Dashboard backfill remained available as a direct skill.
- **Working Modes and Critical Thinking Partner:** functional. Repository/cache and direct copies of `working-modes`, `critical-thinking-partner`, `echo-chamber-drift-check`, and `rapid-iteration-mode` matched.
- **Hyphenomenon:** project intake, chat intake, and usage reporting were present. The report matched `origin/main`; the two intake skills were forward local variants requiring promotion or reconciliation.
- **RPS Etsy and wall art:** present and synchronizable, but production quality is unverified. The enabled plugin source differed from the repository, direct uploader/wall-art skills coexisted with different plugin variants, and historical operator experience reports weak mockup output and insufficiently hardened listing behavior. Installation parity must not be treated as production-readiness evidence.
- **RPS print and Faire:** `rps-print-order` was present as a local-only direct skill. No dedicated Faire-named skill or plugin was found in the audited locations.
- **Design system:** present but disabled; keep inactive until its extra source assets are reviewed.
- **Jamstack:** four direct skills matched their repository direct copies. The duplicate plugin remained inactive, and its formulations were not byte-identical to the direct skills.
- **Project tranche:** direct skill matched the repository; duplicate plugin remained inactive.
- **Motion Design Director:** functional. All nine cached skills matched the repository copy, but the custom marketplace source registration was not reproducible from the audited manifests.
- **Multi-Mailbox Ops:** functional. Plugin source/cache matched. Package and plugin were version 0.1.0. The installed CLI and repository `dist/cli.js` shared SHA-256 `a02cef8c6e9216b9406924ca81d63988be86eee841c2b7d15fc672e64cde9fc8`.
- **TMORA:** `tmora-postcard-production` and `tmora-shopify-product-intake` were local-only; `tmora-print-proof-deck` was a newer divergent local variant.

Two cached Xyppy print-configurator previews were observed. They are preview/cache evidence only, have no source precedence, and must not be treated as production checkout or fulfillment capability.

## Recommended source precedence

1. Use `codex-skills` `origin/main` commit `d8f26f5bf5eb9272b7a1d9dac981aa02891aca26` as the baseline for direct custom skills and the Context Layer, RPS Etsy Ops, Working Modes, Motion, Design System, Jamstack, and Project Tranche plugin directories.
2. Preserve the Air's RPS wall-art guardrail patch from `7dc67f55cf3afa47f162eebad72c8336a9476ce0` as explicit integration input rather than losing it during reconciliation.
3. Preserve and review the newer Air copies of `catalog-review`, both Hyphenomenon intake skills, and `tmora-print-proof-deck`; promote accepted versions into Git before replacing installed copies.
4. Keep MMO locked to Air checkpoint `39db2f161194edd37a0dbf26df3ef63e696da789` until that checkpoint is reviewed and merged.
5. Choose one active lane per overlapping capability: plugin or direct, not both.
6. Treat all plugin caches and Xyppy previews as evidence only. Git-backed sources remain authoritative.
7. Keep portability/parity work separate from RPS workflow hardening. Record broken or suboptimal behavior instead of silently preserving it, and require representative Etsy and Shopify mockup/listing fixtures plus human visual review before assigning a production-ready verdict.
