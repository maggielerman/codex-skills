---
name: motion-design-director
description: "Use when planning, critiquing, refining, or implementing tasteful frontend motion: subtle animation, editorial transitions, GSAP implementation direction, motion critique, too-much-motion review, premium/magical feel, scroll narrative, masking, morphing, parallax, entrance timing, or reduced-motion review."
---

# Motion Design Director

Use this skill as the taste layer for frontend motion. It decides what should move, why it should move, how it should feel, which tokens and patterns fit, and how the result should be reviewed. It does not replace GSAP documentation or bundled GSAP implementation skills.

## Start Here

1. Translate the prompt into motion intent before proposing implementation.
2. Choose one primary taste profile from `references/motion-vocabulary.md`.
3. Select concrete values from `references/motion-tokens.json`.
4. Pick a pattern from `references/motion-patterns.md`.
5. Route GSAP API details through `references/gsap-delegation-map.md` and the bundled official GSAP skills.
6. Review the output with `references/motion-review-rubric.md` and `references/accessibility-performance-policy.md`.

## Motion Intent

Every animation must serve at least one job:

- Direct attention.
- Clarify hierarchy.
- Preserve spatial continuity between states.
- Add tactile feedback.
- Create editorial atmosphere.
- Reward exploration without blocking work.

If the animation does not serve one of these jobs, remove it or make the state change instant.

## Taste Profiles

Pick a profile before implementation:

- Soft
- Tactile
- Editorial
- Magical
- Premium
- Playful
- Cinematic
- Utility

Do not use vague adjectives alone. Pair the profile with timing, easing, distance, stagger, and intensity tokens.

## Implementation Delegation

This skill governs motion taste, intent, sequencing, critique, and refinement. For GSAP mechanics, use the bundled official GSAP skill that matches the problem:

- `gsap-core` for basic tweens, eases, durations, staggers, and defaults.
- `gsap-timeline` for sequencing, labels, nesting, and position parameters.
- `gsap-scrolltrigger` for scroll-linked motion, scrubbing, pinning, refresh, and cleanup.
- `gsap-plugins` for MotionPath, Flip, SplitText, Draggable, Observer, and related plugins.
- `gsap-utils` for value mapping, clamping, snapping, selection helpers, wrapping, and pipes.
- `gsap-react` for React and Next.js lifecycle, refs, scoping, SSR, and cleanup.
- `gsap-performance` for transform-first animation, batching, ScrollTrigger performance, and layout safety.

Do not invent GSAP APIs from memory. If implementation details are uncertain, consult the relevant bundled GSAP skill or canonical GSAP documentation.

## Hard Rules

- Do not recreate GSAP documentation in this skill.
- Do not copy large GSAP docs into the taste layer.
- Do not add motion only because it is possible.
- Do not prioritize spectacle over clarity.
- Do not delay controls behind decorative animation.
- Do not animate every child with identical timing unless the repetition is intentional.
- Do not let decorative lines, paths, masks, or nav motion overlap readable content.
- Do not treat automated tests as enough proof for motion-heavy UI.
- Do not ship motion without reduced-motion behavior.

## Review Contract

For motion-heavy UI, verify the rendered experience, not only the code:

- Desktop and mobile screenshots when practical.
- Console health.
- No framework overlay.
- No clipping, overlap, layout shift, or scroll trap.
- Reduced-motion behavior.
- Interaction responsiveness.
- Whether the motion still feels intentional after half the effects are removed.

## References

- Read `references/motion-taste-runbook.md` for the operating model.
- Read `references/motion-vocabulary.md` for taste profiles.
- Read `references/motion-tokens.json` before choosing values.
- Read `references/motion-patterns.md` before proposing animation behavior.
- Read `references/refinement-playbook.md` when the user says the motion is too generic, too noisy, too slow, cheap, flat, or not magical enough.
- Read `references/anti-patterns.md` before adding expressive motion.
- Read `references/accessibility-performance-policy.md` before implementation or final review.
- Read `references/gsap-delegation-map.md` before writing GSAP code.
