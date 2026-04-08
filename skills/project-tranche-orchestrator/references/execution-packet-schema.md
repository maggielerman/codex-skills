# Execution Packet Schema

Use this as the primary internal contract for one tranche. Keep it ephemeral unless the user explicitly asks to persist it.

## Required shape

```json
{
  "orchestration": {
    "delegation_mode": "collaborative",
    "user_approval_required": true,
    "source_refs": ["DOCS/PROJECTS/active/0123_project.md#Acceptance Criteria"],
    "must_read_files": ["AGENTS.md", "ROADMAP.md", "DOCS/PROJECTS/active/0123_project.md"],
    "drift_triggers": ["Acceptance criteria conflict with repo reality"]
  },
  "project": {
    "id": "0123",
    "title": "Project title",
    "source_doc": "DOCS/PROJECTS/active/0123_project.md",
    "current_status": "active"
  },
  "tranche": {
    "id": "0123-t1",
    "name": "Tranche name",
    "objective": "One-sentence tranche objective",
    "in_scope": ["Bounded deliverable"],
    "non_goals": ["Explicit non-goal"],
    "dependencies": ["Dependency or prerequisite"],
    "blockers": ["Known blocker, if any"],
    "exit_criteria": ["Condition that must be true before review passes"],
    "escalation_conditions": ["Condition that requires user input"],
    "lifecycle_target_after_review": "in-review"
  },
  "assignments": [
    {
      "role": "Worker 1",
      "objective": "Concrete bounded objective",
      "scope": ["Specific change or investigation"],
      "non_goals": ["Do not touch X"],
      "write_paths": ["src/feature-a", "tests/feature-a"],
      "source_refs": ["DOCS/PROJECTS/active/0123_project.md#Next Step"],
      "must_read_files": ["DOCS/PROJECTS/active/0123_project.md", "src/feature-a/index.ts"],
      "acceptance_criteria": ["Observable completion signal"],
      "verification": ["Unit tests", "Focused manual check"],
      "quote_back_required": true,
      "handoff_prompt": "Agent-ready prompt text"
    }
  ],
  "review_gate": {
    "doc_criteria": ["Project doc acceptance criteria satisfied"],
    "code_review_checks": ["No unresolved regression risk"],
    "required_evidence": ["Tests run and summarized"]
  }
}
```

## Field notes

- `orchestration`: mode and anti-drift controls for the primary agent. These guardrails stay lightweight but explicit.
- `project`: identifies the governing project doc and current lifecycle state.
- `tranche`: defines the bounded work unit the primary agent is managing.
- `assignments`: role-based subagent packets. Keep them independent when parallelized and anchored to concrete repo context.
- `review_gate`: explicit evidence required before lifecycle advancement.

## Guardrail guidance

- `delegation_mode`: `collaborative` or `autonomous`.
- `user_approval_required`: usually `true` in `collaborative`, usually `false` in `autonomous`.
- `source_refs`: lightweight citations back to the docs or repo files that justify the packet.
- `must_read_files`: smallest useful set of files that the agent must read before acting.
- `drift_triggers`: reasons to stop, re-read, or escalate instead of pushing ahead on stale assumptions.
- `quote_back_required`: use for risky or ambiguity-prone slices; leave `false` for trivial bounded work.

## Authoring rules

- `source_refs` should be specific enough to re-open the governing source quickly.
- `must_read_files` should stay compact. Include only the files that materially anchor scope or implementation.
- `in_scope`, `non_goals`, `exit_criteria`, `escalation_conditions`, `acceptance_criteria`, and `verification` should all be bullet-sized statements.
- `write_paths` should be as concrete as possible when delegation is parallel.
- If a field is truly unknown, prefer an explicit placeholder like `"Needs repo confirmation"` over silence.
- `lifecycle_target_after_review` should align with the lifecycle rules in `lifecycle-rules.md`.
