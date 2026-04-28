# Agent Prompt Template

Use this prompt shape for one cluster at a time.

## Prompt

You are assigned **Cluster <ID>** in repository `<ABS_REPO_PATH>` on branch `<BRANCH>` and worktree `<ABS_WORKTREE_PATH>`.

### Scope

- Projects: `<PROJECT_IDS>`
- Objective: `<OBJECTIVE>`
- Out of scope: `<OUT_OF_SCOPE>`

### Required context first

1. Read `AGENTS.md`.
2. Read `ROADMAP.md` and `CHANGELOG.md`.
3. Read all project docs for this cluster under `DOCS/PROJECTS/*`.

### Execution rules

- Keep docs + governance in sync with implementation.
- Use checkpoint updates with absolute ET timestamps.
- Do not run destructive git commands.
- Run relevant validation/tests before handoff.

### Deliverables

1. Code/docs updates for scoped projects.
2. Project checkpoint updates with completed work and next targets.
3. Short status summary including:
- files changed
- validations run
- open risks/blockers

### Handoff gate

Do not mark projects as `completed` without collaborative walkthrough/sign-off.
