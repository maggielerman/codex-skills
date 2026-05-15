# Subagent Prompt Template

Use this template when the primary agent delegates a bounded tranche slice.

```text
You are working on one bounded slice of a larger tranche. You are not alone in the codebase, so do not revert work you did not author and keep your changes within the owned surfaces below.

Mode:
- <collaborative or autonomous>

Project:
- ID/title: <project id and title>
- Source doc: <path>

Tranche:
- Name: <tranche name>
- Objective: <one sentence>
- Exit criteria: <one or more conditions>
- Known blockers: <none or list>

Your role:
- <worker role>

Owned scope:
- <bounded item>

Non-goals:
- <explicit non-goal>

Owned write paths:
- <path or surface>

Source refs:
- <doc or file reference that justifies this slice>

Must-read files before acting:
- <governing doc or code file>

Acceptance criteria:
- <criterion>

Verification expected:
- <check>

If `quote_back_required` is true, first reply with:
- your understanding of the owned scope
- the files you intend to touch
- the main thing you will not touch
- one sentence on how you will know you are done

Drift triggers:
- <condition that requires you to pause, re-read, or escalate>

Handoff:
- Summarize what changed
- List files changed
- Note any unresolved risks or blockers
```
