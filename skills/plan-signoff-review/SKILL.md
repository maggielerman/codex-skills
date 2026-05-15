---
name: plan-signoff-review
author: Maggie Lerman
description: Review a proposed final plan against the full current thread and the latest supporting audits, reports, and decision artifacts before approval. Use when the user asks to double-check that a plan reflects everything discussed, incorporates the newest review documents, or needs a final readiness pass in an existing Plan mode thread.
---

# Plan Signoff Review

Rebuild the review from primary source context instead of trusting compressed summaries. Use this only after a draft plan already exists and the thread is already operating in Plan mode.

## Inputs

Read these first when present:
- the full current thread from the first in-scope user message through the latest plan draft
- the most recent version of the plan the user is being asked to approve
- the newest audits, reports, review docs, or checklists referenced in the thread
- any repo governance or source-of-truth documents the thread treats as authoritative

If a referenced artifact cannot be found, call it out explicitly and treat it as a sign-off blocker instead of guessing.

## Workflow

1. Rebuild the thread record.
- Re-read the thread in order. Do not rely on compressed context, memory, or the latest turn alone.
- Extract decisions, constraints, scope commitments, rejected options, dependencies, and promised follow-ups.
- Normalize relative time references into exact dates when the thread makes timing-sensitive claims.

2. Gather the latest supporting artifacts.
- Identify every audit, report, or decision document the thread says should inform the final plan.
- Read the newest available version of each artifact.
- Prefer primary artifacts over later summaries when they disagree.

3. Compare the plan against the record.
- Check that the plan covers every material decision and committed work item.
- Flag stale assumptions, omitted scope, contradictory sequencing, superseded references, and missing acceptance criteria.
- Verify dependencies and ordering still match the latest evidence.

4. Run an independent pass when appropriate.
- If the user explicitly asks for independent review and the current tool policy allows delegation, consider spawning 1-2 subagents.
- Give those reviewers the plan and raw source artifacts, not your conclusions.
- Ask them to look for omissions, contradictions, stale references, and execution risks.
- Reconcile their findings yourself before responding.

5. Return a sign-off review, not a vague summary.
- Lead with concrete gaps and contradictions.
- State which artifacts you verified and which were missing.
- Say clearly whether the plan is ready to approve, needs specific amendments, or is blocked on missing evidence.
- Prefer exact amendment recommendations over a full rewrite unless the user asks for a rewritten plan.

## Output Contract

Return sections in this order:
1. `Coverage Gaps`
2. `Contradictions Or Stale References`
3. `Artifact Freshness Check`
4. `Recommended Plan Amendments`
5. `Approval Recommendation`

For each issue:
- cite the thread message, file, or artifact that supports it
- explain the practical impact on the plan
- give one concrete corrective action

If the plan is fully aligned, say so explicitly and name the artifacts and decisions you verified.

## Hardened Invocation Prompt

`Use this skill to re-read the full current Plan mode thread, compare the latest proposed plan against everything we decided, verify it uses the newest audits and reports, and tell me exactly what must change before I approve it.`
