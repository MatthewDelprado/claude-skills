---
name: squint
description: Design-craft review of a UI. Squints at a screenshot, page, design frame or running app, shows what's off with real-pixel evidence and a rendered fix for each, renders the judgement calls as options to pick, and publishes it all as one visual review page. Its rules live in references/rules.md and grow from the user's own calls over time. Trigger on "squint", "/squint", "give it a squint", "squint at this", "design crit", "critique this UI", "critique this screen". Not for critiquing a design doc or plan (grill-me), code review, PR review, a general "what do you think", or the word "squint" in passing; not for building a screen (mock-up does that).
---

# squint

Designers squint at a screen to blur away the detail and see what actually stands out. Start there, then zoom in. Name what's off, show it, show the fix, and leave the user to steer.

Works in any repo. The rules are in `references/rules.md`. A repo can add its own in `.claude/squint.md` (its tokens, brand rules, things it doesn't care about), and those win over the defaults.

## Stance

- **Squint first.** Before any detail: what do you see first, second and third? Does that order match what the screen is for?
- **System before style.** When something feels off, check the scales first: type sizes, spacing, alignment, colour roles, radii.
- **Say, or ask.** If it's visible and clearly breaks a rule, say it plainly. If it's a judgement call, ask the question that makes them look again.
- **Show, don't describe.** Every finding carries a crop of the real pixels. Every fix and every ask option is rendered, not written up.
- **Tag it.** Every point carries its rule ID, like `(S4 Spacing)`, so it's clear what it rests on.
- **Render, don't change.** Fixes are rendered into the running app for the review only. Nothing lands in the user's code until they pick "Fix it".
- **Direct and specific.** No hedging, no filler praise. If something works, say why.

## Get real pixels

Review what people will see, not what the code suggests. In order:

1. A screenshot, page or frame the user gave.
2. A local or staging URL, or the repo's running app: capture it yourself at desktop and phone width, sharp (2x/3x device scale). Browser-pane screenshots are downscaled; drive the page with the project's Playwright or a headless browser instead. For an iOS app, use the simulator.
3. Code only: say you're reading code, so anything about rendering is a guess, and offer to render it.

Say what you assumed: viewport, scale, data state. If the CSS is in the repo, work contrast out from its colour tokens and say "computed". From a screenshot alone it's "looks under 4.5:1 (estimate)", never a measured ratio. Query the DOM for content the screen hides (truncated, collision-hidden, off-canvas): it doesn't show in pixels.

## Run it

1. **Read it.** One line on what the screen is for and who uses it. If you genuinely can't tell, ask that one thing first.
2. **Squint pass.** What reads first, second, third, and whether that's right.
3. **Walk the rules.** Go through `references/rules.md` (and `.claude/squint.md` if present) silently. Keep only what would most change the next version, starting with whatever stops someone reading or using the screen. At most five **Off** and three **Ask**.
4. **Render.** For each Off, inject the fix into the running page (CSS, a small DOM move, or a patched module served through request interception) and capture the same region before and after. For each Ask, render two or three candidates. For the **Try**, render all the Off fixes together. Recipe in `references/artifact.md`.
5. **Publish** one review page from `references/template.html` (the Artifact tool; load its design guidance first). Recipe and page contract in `references/artifact.md`. The page is private to the user. If the captures show real personal or customer data or secrets, ask before publishing and offer the local file instead.
6. **Reply** in chat with the link and the shape below, short. The page carries the detail.

## Reply

```
**Read:** <the screen's job and who it's for>
**Squint:** <what reads 1st, 2nd, 3rd, and whether that's right>
**Off:** <one line each, with rule IDs>
**Ask:** <the questions, one line each>
**Review page:** <link>. Pick fixes and options there, then say "apply the squint picks".
```

Without an Artifact tool, write the page to `${TMPDIR:-/tmp}/squint/`, never into the repo (it can be megabytes of images), and send it, or fall back to the same shape in chat with the image paths.

## After the user picks

Read the page's picks back with `ArtifactData` (`list` on the `picks` collection). Without `ArtifactData` or the page's `db`, ask the user to say their picks in chat. Then:

- **Fix it**: apply that fix in code as rendered, and run the repo's own checks.
- **It's on purpose**: an overruled finding. Follow it for the session and offer to log it (below).
- **Ask choices and notes**: act on them, or ask one follow-up if a note is unclear.

**On a new version:** re-capture, say what got better and which rule it serves, what's still off, and one new question. Don't start over.

## Rules grow

`references/rules.md` is a starting set. It becomes the user's own over time.

- Rule IDs are permanent: `S1`, `S2`, and so on. Never renumber or reuse one. A dropped rule is marked retired, not deleted.
- When the user overrules a finding ("that's on purpose", "don't flag that") or states a preference ("we always…"), follow it for the rest of the session. Offer once per session: "Log that as a squint rule? (skill-feedback)". It's filed with the signal `new rule` or `overruled`.
- `skill-review squint` folds those issues into `references/rules.md`. A rule the user stated outright needs only one issue.
- A preference that belongs to one repo goes in that repo's `.claude/squint.md` instead.
- Logged rules land in a public repo. Write them generically: no workplace, product, brand or client names.

## Related skills

- `mock-up` sketches a fix only when it can't be rendered into the real app (a new screen, a flow that doesn't exist yet). Label those as mock-ups on the page.
- `skill-feedback` logs new rules and overruled findings; `skill-review` folds them in.

## Anti-patterns

- A findings list in chat with no pictures, or a fix described instead of rendered.
- Before and after taken from different regions, scales or data states.
- Walking every rule out loud, or padding sections to fill them.
- Problems that aren't visible, or exact contrast ratios from a screenshot.
- Changing the user's code before they pick "Fix it".
- Praise without a reason.
- Firing on code review, PR review or a general "what do you think".
