# Refinement Playbook

Use this when the first pass is close but the feel is wrong.

## Too Generic Or Template-Like

- Add hierarchy: primary object leads, secondary objects follow.
- Avoid identical fade-up reveals across every section.
- Change one axis of specificity: mask, path, object continuity, stagger shape, or scroll relationship.
- Use fewer effects with more intentional sequencing.

## Too Noisy

- Remove decorative secondary effects first.
- Shorten or remove delays.
- Reduce distance by one token level.
- Keep text stable.
- Avoid competing parallax, mask, and stagger in the same viewport.

## Too Slow

- Shorten controls to `duration.fast` or less.
- Use `duration.base` only for section-level entrances.
- Use `duration.slow` or `duration.cinematic` only for hero/editorial scenes.
- Remove initial delays above `tasteRules.heroMaxInitialDelay`.

## Cheap Or Bouncy

- Remove elastic/bounce easing unless the profile is explicitly playful.
- Prefer `ease.entrance`, `ease.standard`, or `ease.inOut`.
- Reduce overshoot.
- Reduce travel distance.
- Avoid animating multiple unrelated objects at once.

## Flat Or Static

- Add a small stagger.
- Add subtle depth to media, not body copy.
- Use continuity between source and destination states.
- Let primary objects move slightly more than supporting text.

## Not Magical Enough

- Add coherent transformation: mask, morph, path, reveal, or shared-object continuity.
- Keep the transformation tied to visible cause and effect.
- Reduce unrelated motion while the magical moment happens.
- Verify that surprise does not obscure the content.

## Not Premium Enough

- Cut total effects.
- Use restrained distances.
- Use confident easing.
- Lead with composition and hierarchy, not bounce.
- Make controls immediately usable.
- Confirm the result still feels polished if half the effects are removed.
