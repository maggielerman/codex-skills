# Checkpoint SOP

Use this when adding the no-build policy to a repo's Product OS, checkpoint workflow, or agent instructions.

## Standard Rule

Default no-build policy: commits, pushes, and PR creation must not automatically spend GitHub Actions or hosting build minutes. Run CI, previews, production builds, and deploy smoke tests manually at named checkpoints, then record the run link/result in the owning project doc.

## Recommended Checkpoint Language

Add to `AGENTS.md`:

```md
## CI and Hosting Build-Minute Guardrails

- Default behavior: commits, pushes, and PR creation must not automatically trigger paid GitHub Actions, Vercel, Netlify, Render, or equivalent hosting builds.
- Use manual checkpoint runs for CI and deploys through GitHub `workflow_dispatch`, provider dashboard deploys, deploy hooks, or documented CLI/API commands.
- Run CI/deploy checkpoints when implementation moves to `in-review`, before sign-off, before release merge, before production deploy, or when the user explicitly asks.
- Record checkpoint run links, deploy URLs, failures, and follow-up actions in the owning `DOCS/PROJECTS/` project doc.
- Use `MAGGIE TODO:` for dashboard-only provider settings, billing review, branch-protection updates, or credentials/access that require Maggie.
```

Add to `DOCS/development/checkpoint-workflow.md`:

```md
### Build-Minute Checkpoint Gate

Routine commits and PR updates are no-build events. At each meaningful checkpoint:

1. Name the checkpoint in the project doc.
2. Run the required manual GitHub Actions workflow(s).
3. Trigger only the required preview or production deploy.
4. Paste run links, deploy links, and outcomes into the checkpoint evidence.
5. Move the project lifecycle state only after required manual runs pass or a `MAGGIE TODO:` records the external blocker.
```

Add to active project docs:

```md
## Build/Deploy Checkpoints

- Pending: <checkpoint name> - manual CI/deploy not yet run.
- Evidence: <GitHub Actions run URL>, <deploy URL>, <notes>.
- MAGGIE TODO: <dashboard-only setting or billing/access follow-up, if any>.
```

## Checkpoint Names

Use names that make billing and intent auditable:
- `implementation-complete`
- `in-review-readiness`
- `pre-signoff`
- `pre-merge`
- `release-candidate`
- `production-deploy`
- `post-deploy-smoke`

## Evidence Expectations

At minimum, record:
- workflow name and run URL,
- commit SHA,
- deployment URL or provider event URL,
- pass/fail result,
- manual tester or reviewer when relevant,
- follow-up item for failures or skipped runs.

Do not claim a checkpoint passed only because code was committed. The checkpoint passes when the intentional manual run/deploy succeeds or the user accepts the risk of not running it.
