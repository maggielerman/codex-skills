---
name: cluster-assignment
description: Split repository work into dependency-safe parallel clusters, then bootstrap branches/worktrees, GitHub tracking issues, and ready-to-run agent prompts. Use when a user asks to run multiple agents in parallel or wants branch/worktree cluster setup.
---

# Cluster Assignment

## Overview

Use this skill to convert a prioritized backlog into parallel execution clusters, each with a clean branch/worktree, tracking issue, and a concrete prompt for an agent to execute.

## When To Use

- User asks to run multiple agents in parallel on one repo.
- User asks for branch/worktree setup for project clusters.
- User asks for "what should run simultaneously" across a roadmap.
- User asks for per-cluster GitHub issues and agent-ready prompts.

## Required Behavior

- Read repo planning sources first (typically `ROADMAP.md`, `CHANGELOG.md`, and active/in-review project docs).
- Cluster by dependency boundaries first, not by equal sizing.
- Avoid placing streams that edit the same files in parallel unless the user explicitly accepts merge risk.
- Use branch names prefixed with `codex/`.
- Never run destructive git operations (`reset --hard`, forced cleanups) as part of setup.
- If non-obvious tradeoffs exist (for example, sequence-sensitive migrations), pause and confirm before bootstrapping.

## Workflow

1. Build the candidate stream list.
- Extract active, in-review, and near-term stale backlog streams.
- Record hard dependencies and shared-file collision risk.

2. Design the cluster map.
- Group work into 2-4 dependency-safe clusters.
- For each cluster define: objective, project IDs, branch, worktree path, merge risk, and handoff gate.
- Use [references/cluster-plan-template.md](references/cluster-plan-template.md) for output shape.

3. Bootstrap branches and worktrees.
- Prefer deterministic setup with `scripts/bootstrap_worktrees.sh`.
- Feed a CSV plan using [references/cluster-plan.csv](references/cluster-plan.csv).
- Default base branch is `main` unless user specifies otherwise.

4. Create tracking issues (if `gh` is available and user wants GitHub tracking).
- Open one issue per cluster with scope, deliverables, and acceptance criteria.
- Include branch/worktree paths and explicit out-of-scope notes.

5. Generate per-agent prompts.
- Use [references/agent-prompt-template.md](references/agent-prompt-template.md).
- Keep each prompt scoped to one cluster.
- Include required checkpoints, validation commands, and docs/governance expectations.

6. Return execution-ready status.
- Provide created branches/worktrees/issues.
- List blockers and the exact first command each agent should run.

## Output Contract

Return sections in this order:

1. `Cluster Plan`
2. `Bootstrap Status`
3. `Tracking Issues`
4. `Agent Prompts`
5. `Next Coordination Checkpoint`

## References

- Plan template: [references/cluster-plan-template.md](references/cluster-plan-template.md)
- CSV input template: [references/cluster-plan.csv](references/cluster-plan.csv)
- Prompt template: [references/agent-prompt-template.md](references/agent-prompt-template.md)
- Setup helper: `scripts/bootstrap_worktrees.sh`
