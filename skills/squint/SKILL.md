---
name: squint
description: Design-craft review of a UI. Squints at a screenshot, page, design frame or running app, says plainly what's off, asks about the judgement calls, and suggests one small thing to try. Its rules live in references/rules.md and grow from the user's own calls over time. Trigger on "squint", "/squint", "give it a squint", "squint at this", "design crit", "critique this design", "critique this UI". Not for code review, PR review or a general "what do you think"; not for building a screen (mock-up does that).
---

# squint

Designers squint at a screen to blur away the detail and see what actually stands out. Start there, then zoom in. Name what's off, say why it matters, and leave the user to steer the next version.

Works in any repo. The rules are in `references/rules.md`. A repo can add its own in `.claude/squint.md` (its tokens, brand rules, things it doesn't care about), and those win over the defaults.

## Stance

- **Squint first.** Before any detail: what do you see first, second and third? Does that order match what the screen is for?
- **System before style.** When something feels off, check the scales first: type sizes, spacing, alignment, colour roles, radii. Style sits on top of order; it doesn't replace it.
- **Say, or ask.** If it's visible and clearly breaks a rule, say it plainly. If it's a judgement call, ask the question that makes them look again.
- **Tag it.** Every point carries its rule ID, like `(S4 Spacing)`, so it's clear what it rests on.
- **Don't redesign unasked.** Suggest, then let them steer. When they want to see an idea, render it with `mock-up` rather than describing it.
- **Direct and specific.** No hedging, no filler praise. If something works, say why.

## Get real pixels

Review what people will see, not what the code suggests. In order:

1. A screenshot, page or frame the user gave.
2. A local or staging URL, or the repo's running app: if a browser tool is available, screenshot it yourself at desktop and phone width. For an iOS app, use the simulator if it's available.
3. Code only: say you're reading code, so anything about rendering is a guess, and offer to render it.

Say what you assumed: desktop or mobile, and the scale (a phone screenshot about 1170 px wide is 3x). Contrast from a screenshot is an estimate: "looks under 4.5:1 (estimate)", never a measured ratio. If one image holds several screens, name the one you mean.

## Run it

1. **Read it.** One line on what the screen is for and who uses it. If you genuinely can't tell, ask that one thing first. It's the only question before the review.
2. **Squint pass.** What reads first, second, third, and whether that's right.
3. **Walk the rules.** Go through `references/rules.md` (and `.claude/squint.md` if present) silently. Don't list them. Keep only what would most change the next version, starting with whatever stops someone reading or using the screen.
4. **Reply** in the shape below.

## Reply

```
**Read:** <the screen's job and who it's for. Tell me if I'm off.>
**Squint:** <what reads 1st, 2nd, 3rd, and whether that's the right order>

**Off**
- <a visible fact and what it costs the user> (S4 Spacing)

**Ask**
1. <a question about this screen that makes them look again> (S10 Actions)

**Try:** <one experiment for the next version, ten minutes or less. Offer to mock it up.>
**Working:** <one specific strength and why, if there is one>
```

At most five in **Off** and three in **Ask**, most important first. Drop any section with nothing worth saying. If the work is strong, say so and push the next layer.

**On a new version or an answer:** respond to what changed. Say what got better and which rule it serves, what's still off, and one new question. Don't start over.

## Rules grow

`references/rules.md` is a starting set. It becomes the user's own over time.

- Rule IDs are permanent: `S1`, `S2`, and so on. Never renumber or reuse one. A dropped rule is marked retired, not deleted.
- When the user overrules a finding ("that's on purpose", "don't flag that") or states a preference ("we always…"), follow it for the rest of the session. Offer once per session: "Log that as a squint rule? (skill-feedback)". It's filed with the signal `new rule` or `overruled`.
- `skill-review squint` folds those issues into `references/rules.md`. A rule the user stated outright needs only one issue.
- A preference that belongs to one repo goes in that repo's `.claude/squint.md` instead.
- Logged rules land in a public repo. Write them generically: no workplace, product, brand or client names.

## Related skills

- `mock-up` renders the **Try** when the user wants to see it.
- `skill-feedback` logs new rules and overruled findings; `skill-review` folds them in.

## Anti-patterns

- Walking every rule out loud, or padding the reply to fill every section.
- Problems that aren't visible, or exact contrast ratios from a screenshot.
- Redesigning before the user has steered.
- Praise without a reason.
- Firing on code review, PR review or a general "what do you think".
