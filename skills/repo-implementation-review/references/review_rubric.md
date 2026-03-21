# Repo Review Rubric

Use this rubric to score each implementation consistently on outcomes and verified behavior. Score on a 1-5 scale.

## Principle

Do not score based on specific technology choices (for example Notion vs Neon, Cloudflare vs Express).  
Score based on whether the implementation meets the same starting goal and can prove it works.

## Scoring Anchors

- 5: Goal clearly met, behavior verified, low delivery risk
- 4: Goal mostly met, minor verified gaps
- 3: Partially met, meaningful unverified areas or tradeoffs
- 2: Major gaps or low verification confidence
- 1: Goal not met or high operational risk

## Mandatory Evidence Collection

For each repo, collect objective evidence before scoring:

1. Starting goal + intended outcomes
- Read README and core docs (`DOCS/` or `docs/`).
- Capture what the repo claims to accomplish.

2. Docs quality and alignment
- Evaluate whether docs are complete, current, and specific.
- Check whether docs match actual code paths and commands.

3. Automated checks
- Run available tests.
- Run available build/typecheck/lint commands.
- Record pass/fail/skip with command output.

4. Endpoint behavior
- Discover key endpoints from source.
- Probe runnable endpoints when possible.
- Record reachable/unreachable status and errors.

## Dimensions

## 1) Goal Completion

Assess how completely the implementation achieves the stated starting goal.

Evidence prompts:
- Does it implement the required end-to-end workflow?
- Are critical outcomes demonstrably present?
- What is missing versus the intended result?

## 2) Correctness

Assess functional reliability of key paths.

Evidence prompts:
- Do tests and checks support correctness claims?
- Are key error paths handled?
- Are outputs consistent with expected behavior?

## 3) Verification Confidence

Assess confidence level from executable evidence.

Evidence prompts:
- Are automated tests meaningful and run in CI?
- Are check commands repeatable?
- Are endpoint probes successful for expected routes?

## 4) Maintainability

Assess readability, modularity, and onboarding cost.

Evidence prompts:
- Is the architecture coherent for future iteration?
- Is code organization understandable?
- Can new contributors follow docs and workflows?

## 5) Delivery Readiness

Assess real-world operability and risk to ship.

Evidence prompts:
- Are run/deploy workflows clear?
- Are dependencies/secrets/config managed safely?
- Is there enough observability and operational guidance?

## 6) Security

Assess baseline security posture.

Evidence prompts:
- Are auth/authz boundaries clear where needed?
- Are secrets handled without hardcoding/exposure?
- Is input validation present on critical boundaries?

## Comparison Guidance

After individual scoring:
- Compare by outcomes and verified behavior, not by stack preference.
- Highlight where one repo succeeds on goal completion and another does not.
- Call out evidence quality gaps (tests/docs/endpoints) as first-order risks.
- Recommend one path (or hybrid) with concrete 1-2 iteration next steps.
