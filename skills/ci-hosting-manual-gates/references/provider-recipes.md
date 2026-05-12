# Provider Recipes

Use this file only after the repo audit identifies one of these providers. Verify current official docs before live dashboard changes or API work.

## GitHub Actions

Goal: commits, pushes, and PRs do not automatically run expensive workflows.

Preferred file changes:
- Preserve workflows under `.github/workflows/`.
- Add `workflow_dispatch` with explicit `checkpoint`, `scope`, and `reason` inputs.
- Remove broad `push` and `pull_request` triggers from expensive workflows.
- Keep `workflow_call` for reusable workflows.
- Keep `schedule` only for intentionally periodic maintenance that the user approves.
- Keep `release`, tag, or environment deployment triggers only when they are the chosen checkpoint mechanism.

Do not use commit-message skip phrases as the primary policy. GitHub supports them for `push` and `pull_request`, but skipped required checks can remain pending and block PRs.

Manual run options:
- GitHub Actions tab
- `gh workflow run <workflow.yml> -f checkpoint=<id> -f scope=standard -f reason="<reason>"`
- REST API workflow dispatch

Branch protection checklist:
- Remove disabled automatic workflow names from required checks.
- If a check is still required, make sure it can be run manually and reported before merge.
- If a repo requires status checks on every PR update, ask before changing the cost policy because this conflicts with no-build-by-default.

Official docs verified 2026-05-06:
- https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs

## Vercel

Goal: Git-connected commits and PRs do not automatically create Vercel builds.

Preferred file-backed gate:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "git": {
    "deploymentEnabled": false
  }
}
```

Notes:
- `git.deploymentEnabled: false` disables automatic deployments for the project.
- `github.enabled` is legacy/deprecated for this purpose; prefer `git.deploymentEnabled`.
- Manual checkpoint deploy paths can use the Vercel dashboard, deploy hooks, REST API, or `vercel` CLI.
- If using manual CLI deploys, document whether checkpoint deploys should be preview or production.
- If a project needs previews only on release branches, use branch-specific rules instead of disabling everything, but default to all-off for this skill.

Official docs verified 2026-05-06:
- https://vercel.com/docs/project-configuration/git-configuration
- https://vercel.com/docs/builds
- https://vercel.com/docs/deployments/git

## Netlify

Goal: normal Git pushes do not spend Netlify build minutes.

Strongest dashboard gate:
- Project configuration > Build & deploy > Continuous deployment > Build settings > Build status: Stopped builds.

Tradeoff:
- Stopped builds prevent production deploys, Deploy Previews, branch deploys, build hooks, API build triggers, and UI build triggers from building the site. Use this only when local/CLI/manual deploy without Netlify build is acceptable.

File-backed selective gate:

```toml
[build]
  ignore = "node scripts/netlify-ignore-build.mjs"
```

Then create a tiny script that exits `0` for normal Git-triggered builds and exits `1` only for an explicit checkpoint condition. Netlify's ignore command semantics are inverted from many tools: exit `0` stops the build; exit `1` allows the build to continue.

Use `ignore` when:
- build hooks or manual/API deploys still need to work,
- only some branches/checkpoints should build,
- the repo needs a reversible file-backed policy.

Official docs verified 2026-05-06:
- https://docs.netlify.com/build/configure-builds/ignore-builds/
- https://docs.netlify.com/build/configure-builds/stop-or-activate-builds/
- https://docs.netlify.com/deploy/deploy-overview

## Render

Goal: pushes to linked branches do not automatically rebuild/redeploy services.

Preferred controls:
- Dashboard: service Settings > Auto-Deploy > Off.
- Blueprint: set `autoDeploy: false` for services in `render.yaml` when the service is managed from a Blueprint.

Manual checkpoint deploy options:
- Dashboard Manual Deploy
- Render CLI
- deploy hook
- Render API trigger deploy endpoint

Notes:
- Render's default for linked repos is auto-deploy on commit.
- Render also supports skip phrases such as `[skip render]`, but that should be fallback behavior rather than the default operating model.
- If using "After CI Checks Pass", remember that zero checks means no deploy. This can pair with manual CI but is usually less clear than Auto-Deploy Off.

Official docs verified 2026-05-06:
- https://render.com/docs/deploys
- https://render.com/docs/deploy-to-render

## Other Hosts

Apply the same control pattern:
- Identify Git-triggered deploy/build settings.
- Disable deploy-on-push and deploy-on-PR by default.
- Add a manual deploy path that can be run at checkpoints.
- Document the exact command, dashboard path, hook, or API endpoint.
- Leave a `MAGGIE TODO:` if credentials, billing permissions, team owner access, or dashboard-only changes block completion.
