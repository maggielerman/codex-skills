---
name: ci-hosting-manual-gates
description: Convert repositories from automatic CI and hosting builds to checkpoint-driven manual gates. Use when asked to reduce GitHub Actions, Vercel, Netlify, Render, or similar hosting build minutes; disable automatic builds on commit, push, or pull request; preserve frequent commits and PRs without spending CI/deploy minutes; add manual workflow_dispatch actions, deploy hooks, or checkpoint SOPs; or bake build-minute guardrails into Product OS/checkpoint workflows.
---

# CI Hosting Manual Gates

## Overview

Set repository CI and hosting providers so normal commits, pushes, and PR creation do not automatically spend build minutes. Replace automatic behavior with explicit checkpoint-triggered CI and deploy runs, then document the new operating rule in the repo's Product OS or agent instructions.

## Default Policy

- Treat frequent commits, branch pushes, and PR creation as no-build events.
- Run GitHub Actions, deploy previews, production builds, smoke tests, and paid hosting builds only at meaningful checkpoints.
- Prefer manual triggers that are obvious to humans and agents: GitHub `workflow_dispatch`, provider dashboard manual deploys, provider deploy hooks, or CLI deploy commands.
- Keep security scanning, dependency alerts, and required compliance checks separate from cost-heavy build/deploy workflows. Do not disable security controls just to save build minutes.
- If a repo has branch protection or required checks, update those rules before removing automatic PR/push workflows. Otherwise skipped or absent checks can block merges.

Meaningful checkpoints usually include:
- implementation complete and moving to `in-review`,
- before a human walkthrough/sign-off,
- before merging a release PR,
- before production deploy,
- after dependency, infrastructure, auth, payment, data migration, or routing changes,
- when the user explicitly requests a build, CI run, preview, or deploy.

## Workflow

1. Run the audit script from this skill:

```bash
python3 <skill_dir>/scripts/audit_build_triggers.py --repo /path/to/repo
```

Use the output to identify `.github/workflows/`, `vercel.json`, `netlify.toml`, `render.yaml`, package scripts, and hosting config files that may trigger builds automatically.

2. Inspect the repo manually for provider clues:

```bash
rg -n "vercel|netlify|render|deploy hook|workflow_dispatch|pull_request|push|autoDeploy|deploymentEnabled|ignore =" .
```

3. Read only the reference needed for the provider being changed:
- Provider recipes: `references/provider-recipes.md`
- Product OS/checkpoint SOP: `references/checkpoint-sop.md`

4. Patch local repo files with safe-write behavior:
- Add `workflow_dispatch` to expensive GitHub Actions workflows.
- Remove or narrow `push` and `pull_request` triggers from expensive workflows unless the user explicitly wants an automatic exception.
- Add manual deploy commands or docs for the detected hosting provider.
- Add repo-local instructions that default pushes and PRs are no-build events.
- Add `MAGGIE TODO:` callouts for dashboard-only settings that cannot be changed from files.

5. Record the operating rule where agents will see it:
- `AGENTS.md`
- `DOCS/development/checkpoint-workflow.md` or the repo's equivalent
- the active project doc under `DOCS/PROJECTS/`
- `ROADMAP.md` or `CHANGELOG.md` only when the change affects release process materially

6. Verify before finishing:
- normal `git commit` and `git push` no longer trigger expensive workflows by config,
- GitHub workflows still have an explicit manual path,
- hosting providers have either file-backed manual gates or visible `MAGGIE TODO:` dashboard steps,
- required checks/branch protection are not left pointing at removed automatic jobs,
- checkpoint docs say when and how to run CI/deploys.

## GitHub Actions Pattern

For expensive workflows, prefer:

```yaml
on:
  workflow_dispatch:
    inputs:
      checkpoint:
        description: "Checkpoint or project id"
        required: true
        type: string
      scope:
        description: "What to run"
        required: true
        default: "standard"
        type: choice
        options:
          - standard
          - full
          - deploy-readiness
```

Keep reusable workflows available through `workflow_call` when other manual workflows compose them. Avoid relying on commit-message skip phrases as the main policy; they are easy to forget and can leave required checks pending.

## Hosting Provider Pattern

- Vercel: prefer `git.deploymentEnabled: false` in `vercel.json` when the repo owns Vercel config. Use manual dashboard deployments, deploy hooks, or CLI deployments for checkpoints.
- Netlify: prefer stopped builds in the dashboard when all Git-triggered builds should stop. If builds must remain active for hooks, use `[build].ignore` in `netlify.toml` to skip normal Git-triggered builds and allow intentional hook/API/manual deploys.
- Render: prefer Auto-Deploy `Off` in the dashboard or `autoDeploy: false` in `render.yaml` blueprints when present. Use manual deploy, deploy hook, CLI, or API at checkpoints.
- Other providers: find the Git integration setting that deploys on push/PR and turn it off or gate it behind manual deployment, deploy hooks, tags, releases, or approved environments.

## Product OS Integration

When the repo uses `$product-operating-system-scaffold`, add this as a checkpoint rule:

> Default no-build policy: commits, pushes, and PR creation must not automatically spend GitHub Actions or hosting build minutes. Run CI/deploys manually at named checkpoints and record the run link/result in the owning project doc.

Use `MAGGIE TODO:` for any manual provider dashboard work, billing review, or branch-protection change that cannot be completed from the local repo.

## Sources To Recheck

Provider controls change. Before making live provider changes, verify current official docs for the relevant provider and favor primary documentation over memory:
- GitHub Actions workflow syntax and manual runs
- Vercel Git configuration
- Netlify ignore/stopped builds
- Render auto-deploy/manual deploys
