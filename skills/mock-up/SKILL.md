---
name: mock-up
description: Build a throwaway HTML preview of a UI idea in the current repo's own look and feel. Use for "mock this up", "sketch this screen", "what would this look like", "try a layout", or when a UI idea needs seeing rather than describing. For explaining code or flows, use explain-code instead.
---

Make a quick, disposable mockup the user can look at in a browser, styled like the repo they are working in. Skip the preamble.

## Steps

1. Work out the look and feel. Follow `references/look-and-feel.md` for the evidence order and the tie-break.
2. Read the real tokens and two or three real components nearest the work. Use real values from the repo. Never invent colours, type or spacing.
3. Write one self-contained `.html` file. CSS variables in `:root` come from the repo's tokens, markup is shaped like the real components, labels and sample data are realistic, and it works on desktop and mobile. Inline CSS and JS only. No build step, no network calls.
4. Save it to `${TMPDIR:-/tmp}/mock-up/mock-up-{description}.html`. Iterating on the same idea in the same session overwrites the file, so a browser refresh shows the change. A new idea gets a new file name.
5. Open it once: `open "$f" 2>/dev/null || xdg-open "$f" 2>/dev/null || start "" "$f"`. After that, the user refreshes.
6. Say in one line which design system you used and how to switch, every time. Example: `Used <system A> (migration target). Say "use <system B>" to switch.`

## When static will struggle

Build the static version first. Then, if any of these apply, add one line offering more:

- the point of the mockup is behaviour: states, flows, validation, drag, animation
- a hard widget is involved: data grid, chart, rich text editor, date picker
- styles live in a runtime (CSS-in-JS, theme provider), so tokens are not plain values
- no design system was found, so you are guessing
- the screen needs more than a handful of components copied

Offer only what exists here: the repo's Storybook or dev server (look for a `storybook` or `dev` script in `package.json`), or Figma when a Figma connector is available. Example: `Rough: this uses a data grid, which static HTML can't show. Want me to try the real one via Storybook?`

## Sharing

The file lives in a temp folder. If the user wants to show someone, copy it where they say.

## Related skills

- The question is about logic, flow or code structure, not how it looks: use `explain-code`.
- Something here was wrong or missing: `skill-feedback` logs it.

## Feedback

End with one line, "Want me to log that? (skill-feedback)", only when one of these happened this turn, and at most once per session:

- the user asked for a different layout or system straight after
- the user trimmed or corrected the output
- nothing fit and you improvised
- you had to guess between design systems or components
- a hand-off to a sibling skill was redirected

Say nothing when none applied. A user who moves on without comment is not a signal.
