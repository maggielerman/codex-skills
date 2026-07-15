# GSAP Delegation Map

This plugin bundles official GSAP skills as the implementation layer. Use this taste skill to decide what the motion should do and how it should feel; use the GSAP skills for API correctness.

## Routing

| Problem | Use bundled skill |
| --- | --- |
| Basic tweens, duration, ease, stagger, defaults | `gsap-core` |
| Sequencing, labels, nesting, position parameters | `gsap-timeline` |
| Scroll-linked motion, scrub, pin, refresh, cleanup | `gsap-scrolltrigger` |
| MotionPath, Flip, SplitText, Draggable, Observer, plugin selection | `gsap-plugins` |
| Clamp, mapRange, normalize, snap, toArray, selector, wrap, pipe | `gsap-utils` |
| React, Next.js, refs, scoping, SSR, cleanup | `gsap-react` |
| Transform-first animation, batching, layout safety, ScrollTrigger performance | `gsap-performance` |
| Vue, Svelte, or other framework lifecycle patterns | `gsap-frameworks` |

## Rules

- Do not invent GSAP APIs from memory.
- Do not copy large GSAP documentation into this taste skill.
- Use official GSAP skills or canonical GSAP docs when syntax, plugin names, cleanup, licensing, or framework behavior is uncertain.
- Prefer tokenized values from `motion-tokens.json`, then express them through GSAP mechanisms such as timeline defaults or project-local animation helpers.
- If a project already has motion tokens or animation utilities, map this skill's taste tokens onto the existing system instead of adding a parallel runtime.

## Implementation Handoff Shape

When handing off to GSAP implementation, state:

- Intent.
- Taste profile.
- Pattern.
- Tokens.
- Reduced-motion strategy.
- GSAP skill to consult.
- Rendered QA checks required.
