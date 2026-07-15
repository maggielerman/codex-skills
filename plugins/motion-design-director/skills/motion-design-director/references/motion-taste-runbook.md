# Motion Taste Runbook

Motion should feel intentional before it feels impressive. The best outcome is not the most animated interface; it is the interface where motion clarifies meaning, creates a distinctive editorial rhythm, and disappears before it becomes friction.

## Operating Model

1. State the motion intent in one sentence.
2. Choose a taste profile.
3. Choose a pattern.
4. Select token values.
5. Implement through the relevant GSAP skill or existing project animation system.
6. Verify the rendered result.
7. Refine against the rubric.

## Intent Checklist

Use motion when it does at least one of these:

- Directs attention to the next meaningful object.
- Clarifies hierarchy between primary and secondary content.
- Shows continuity between states, pages, cards, panels, or objects.
- Adds tactile feedback to user input.
- Creates editorial atmosphere without blocking comprehension.
- Rewards exploration while preserving control responsiveness.

Avoid motion when:

- It delays access to navigation, filters, forms, or primary actions.
- It repeats the same reveal on every section with no hierarchy.
- It makes dense operational UI feel slower.
- It creates overlap, clipping, scroll traps, or layout shift.
- It only exists to make the page feel less empty.

## Editorial Motion Principles

- Primary objects lead. Secondary details follow.
- Body text moves less than headlines and media.
- Controls should stay available before decorative motion finishes.
- Masking, morphing, and path motion need a visible cause-and-effect relationship.
- Scroll narratives need enough distance to read, but not so much pinning that the page feels captured.
- Premium motion is usually restrained, confident, and specific.
- Magical motion should transform coherently; surprise without continuity reads as random.

## Feedback Translation

When the user says:

- "Too template-y": reduce generic fade-up repetition, add hierarchy, use more specific sequencing or masking.
- "Too much": cut secondary effects first, shorten delays, reduce distance, simplify scroll coupling.
- "Flat": add small hierarchy through stagger, depth, continuity, or tactile input response.
- "Cheap": remove bounce/noisy easing, reduce distance, avoid simultaneous motion on many objects.
- "More premium": use restrained distance, confident easing, asymmetric sequence, and fewer total effects.
- "More magical": add a coherent transformation, mask, path, or continuity move that reveals meaning.
- "Editorial": use staged reveals, strong object hierarchy, scroll composition, and selective masking.

## Verification Standard

Motion-heavy work requires rendered proof. Automated tests and builds are necessary, but not sufficient. Capture or inspect the actual page at desktop and mobile widths when practical, check reduced-motion behavior, and look for overlap, clipping, layout shift, unreadable text, scroll traps, and console errors.
