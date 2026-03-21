---
name: project-governance-audit
description: Run a governance audit across project planning docs and roadmap artifacts. Use for blocker/dependency/order analysis, strategy consistency checks, and checkpoint-quality enforcement with file-backed evidence.
---

# Project Governance Audit

Audit non-completed project streams and roadmap sequencing with a deterministic, evidence-first workflow.

## Inputs

Read these first when present:
- `AGENTS.md` for local governance rules.
- `CHANGELOG.md` for sequencing decisions and recent direction changes.
- `ROADMAP.md` for active execution order.
- `DOCS/PROJECTS/*` or `docs/PROJECTS/*` for status-scoped project docs.
- `DOCS/project-master.md` or `docs/project-master.md` for strategic scope/source-of-truth statements.

Default scope:
- Include all project statuses except `completed`.
- Exclude `completed` unless user explicitly requests it.

Optional portfolio mode:
- If user requests multi-repo governance audit, repeat workflow per repo and then add cross-repo conflict/dependency findings.

## Workflow

1. Confirm structure and status folders.
- Discover project docs root and status directories.
- Build review set from non-completed statuses.
- Record missing expected inputs as blockers.

2. Build a project register.
For each in-scope project capture:
- project id and title
- status folder
- explicit dependencies/gates
- blockers/risks
- latest checkpoint timestamp
- next checkpoint action

3. Validate checkpoint hygiene.
- Flag missing absolute timestamps.
- Flag relative time phrasing (`today`, `tomorrow`, `yesterday`) when governance forbids it.
- Flag missing “completed since prior checkpoint” or missing “next before next checkpoint”.

4. Validate docs governance contract.
- Verify docs root is explicit and consistent in governance docs.
- Verify `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md` align on active execution order.
- Verify docs CI regeneration workflow presence when docs tooling/docs-site policy requires it.

5. Detect within-project issues.
- Missing or vague blockers.
- Missing dependencies for work that is clearly gated.
- Missing success criteria or undefined end-state.

6. Detect cross-project inconsistencies.
- Overlapping scope likely to produce rework.
- Strategy contradictions across active/backlog docs.
- Dependency contradictions vs roadmap order.

7. Reassess roadmap order.
- Separate mandatory reorder (dependency/blocker required) from optional optimization.
- Preserve locked baselines unless explicit trigger conditions are documented.

8. Produce amendment recommendations.
- Recommend minimal edits to remove conflicts.
- Specify exact docs and fields to update.
- Include evidence-backed rationale.

## Quick Commands

```bash
rg --files | rg '(^|/)(AGENTS\.md|CHANGELOG\.md|ROADMAP\.md)$'
rg --files | rg '(^|/)(DOCS|docs)/(PROJECTS|projects)/'
rg -n -i 'blocker|blocked|risk|dependency|depends on|gated on|after|conflict|strategy|checkpoint|next before next checkpoint' DOCS docs
```

## Output Contract

Return findings in this order:
1. `Critical blockers`
2. `Conflicts/inconsistencies`
3. `Roadmap reorder recommendations`
4. `Amendments to apply`
5. `Next checkpoint plan`

For each finding:
- Include severity (`high`, `medium`, `low`).
- Include file-backed evidence.
- Include one concrete corrective action.

For next checkpoint plan:
- Use absolute timestamps.
- State completed work since prior checkpoint.
- State what happens before the next checkpoint.

## Hardened Invocation Prompt

`Review all project docs across every status except completed. Identify blockers, dependency/order problems, checkpoint hygiene issues, and conflicting strategies. Then review the roadmap and propose exact reordering plus doc amendments with file-backed evidence and a next-checkpoint plan.`
