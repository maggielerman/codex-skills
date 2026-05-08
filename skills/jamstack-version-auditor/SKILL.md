---
name: jamstack-version-auditor
description: 'Repo-aware version and upgrade assessment for JAMstack/frontend stacks. Use when checking Tailwind CSS, Eleventy/11ty, Build Awesome, Nunjucks, Alpine.js, PostCSS, Vite, Node, deployment, or static-site repo versions, latest stable releases, docs currency, or upgrade value.'
---

# JAMstack Version Auditor

Use this skill to make version awareness part of JAMstack work. The goal is not "always upgrade"; the goal is to know what the repo uses, know what is current, and make a careful recommendation.

## Start Here

1. Inspect the repo's actual dependency state before giving version advice:
   - `package.json`
   - lockfile: `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, or `bun.lock`
   - Node/runtime files: `.nvmrc`, `.node-version`, `engines`, CI config, deploy config
   - framework config: Tailwind CSS entry/config, Eleventy config, PostCSS/Vite/build config, Alpine import/CDN usage
2. Identify the package manager from the lockfile and scripts. Use the repo's package manager for all checks.
3. Query current stable releases at task time. Do not rely on this skill's creation date or model memory.
4. Compare installed/resolved versions with `latest`, not prerelease tags, unless the repo already opts into prereleases.
5. Recommend an update only when the evidence supports it.

## Current-Version Commands

Prefer package-manager-native commands:

```bash
npm view tailwindcss version dist-tags --json
npm view @tailwindcss/cli version dist-tags --json
npm view @11ty/eleventy version dist-tags --json
npm view alpinejs version dist-tags --json
npm view @upstash/context7-mcp version dist-tags --json
npm view mcp-remote version dist-tags --json
```

For broader repos, inspect relevant installed and latest versions:

```bash
npm outdated --json
pnpm outdated --format json
yarn outdated --json
bun outdated
```

If the repo uses another registry, workspace catalog, overrides, resolutions, or vendored dependencies, inspect those before comparing versions.

## Recommendation Policy

Suggest updating when one or more are true:

- The installed version is behind the current stable major and the repo is starting new work, already doing dependency maintenance, or needs features/fixes from the newer major.
- Security advisories, deprecations, Node/runtime support, browser support, or deployment constraints make the current version risky.
- The user specifically asks for modernization, latest docs, migration, or current best practices.
- The repo mixes docs/config from a newer major with dependencies from an older major.
- A bug or build issue is likely fixed by a known newer stable release.

Do not suggest updating as a reflex when:

- The repo is stable, the requested task is unrelated, and the dependency is only one patch/minor behind.
- The update is a major migration with meaningful config, runtime, CSS output, or plugin risk.
- The deployment environment or Node version cannot support the latest stable release.
- The repo intentionally pins an older major such as Tailwind v3 LTS or a framework version required by a theme/plugin.
- The change would expand scope beyond the user's task without clear benefit.

When unsure, present the update as optional maintenance, not a prerequisite.

## Stack-Specific Checks

For Tailwind CSS:

- Detect v4 vs v3 from dependencies and files: `@import "tailwindcss"`, `@theme`, `@source`, `@tailwind` directives, `tailwind.config.*`, PostCSS config, CLI usage.
- Compare `tailwindcss`, `@tailwindcss/cli`, `@tailwindcss/postcss`, `@tailwindcss/vite`, and relevant plugins.
- Treat v3 to v4 as a migration, not a routine patch update. Check official upgrade docs and plugin compatibility first.
- Keep `tailwindcss-expert` active for implementation details.

For Eleventy:

- Compare `@11ty/eleventy` against the stable `latest` dist tag.
- Treat Build Awesome v4 as the announced continuation path for Eleventy v4, but do not recommend prerelease/canary migration unless explicitly requested or already adopted by the repo.
- Note prerelease/canary versions separately. Do not recommend canary unless the repo already uses canary or needs a canary-only fix.
- Check Node version requirements, config module format, plugins, transforms, filters, shortcodes, image plugin, RSS/navigation plugins, and hosting build command.
- Keep `eleventy-jamstack-expert` active for architecture changes.

For Alpine.js:

- Compare npm dependency or CDN URL version with the current stable package.
- Check plugins such as `@alpinejs/collapse`, `@alpinejs/focus`, `@alpinejs/persist`, and CSP build usage.
- Alpine patch/minor updates are often low-friction, but still test interactive states and CSP behavior.
- Keep `alpinejs-lightweight-js` active for implementation details.

For broader JAMstack tech:

- Inspect Vite, PostCSS, Lightning CSS, Browserslist, Autoprefixer, Sass, Markdown/MDX, Nunjucks, image plugins, sitemap/RSS tools, deployment adapters, and Node.
- Prioritize updates that affect build correctness, security, deploy support, or compatibility with the touched framework.

## Documentation Policy

- Use MCP docs when available: Context7 for versioned library documentation and GitMCP for current repository docs/source.
- If MCP is unavailable, use primary docs or npm registry data.
- Confirm current dates and versions when writing migration advice.
- Cite or name the source of version truth in the response when the user asks for a version decision.

## Output Standard

Give a short audit summary:

- Current repo versions found
- Current stable versions checked
- Recommendation: update now, update later, no update needed, or investigate first
- Why: compatibility, risk, benefit, migration size
- Next steps: exact package-manager command or migration doc to follow, only when an update is recommended

Never silently upgrade dependencies unless the user asked you to perform the update.

## References

Read `references/version-checks.md` for command patterns, package-name coverage, and migration-risk notes.
