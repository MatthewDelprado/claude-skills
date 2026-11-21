# squint review page

How squint captures evidence, renders fixes and publishes the review. The page itself is `template.html` in this folder: copy it, fill its data, publish.

## Capture

Use the repo's own Playwright if it has one (import it by absolute path from the main checkout's `node_modules`), else a headless browser. The browser pane's screenshots are downscaled and lose detail, so use them only to look around.

- **Sizes.** Desktop 1440 × 900 at device scale 2. Phone 390 × 844 at scale 3 with `isMobile` and `hasTouch`. Add the repo's own breakpoints if `.claude/squint.md` names them.
- **Settle.** Wait for the app's own ready signal (a `window` hook, a `ready` class, or network idle), then stop anything animating or growing, then wait a beat. Before and after must show the same data state.
- **One fresh page per fix.** A new browser context for each, so fixes don't stack and the before is always clean.
- **Same clip.** Capture the before, apply the fix, capture the same `clip` region again. Clip to the region the finding is about; use the full viewport only for hierarchy findings.
- **Hidden content.** Pixels can't show what the screen hides. Query the DOM for elements hidden by collision, truncation or `visibility`, and count them. "7 of 28 labels hidden" is a finding a screenshot never shows.
- **Contrast.** Work it out from the CSS colour tokens, including alpha and any `opacity` on the element (component libraries often dim disabled controls to 50%). Say "computed". Without source, say "estimate".
- **Size budget.** Save as progressive JPEG at quality ~82: full views 1600 px wide, panel crops at native size. A review page should stay under ~2 MB.

## Render the fix

Pick the lightest way that renders the real thing:

1. **CSS** injected with a `<style>` tag: colour, size, spacing, hierarchy, visibility.
2. **DOM moves** in `page.evaluate`: moving an icon to another column, adding a pinned footer that calls the original button's click.
3. **A patched module** through request interception (`page.route` on the module's URL, edit the response text, `fulfill`): layout constants, a default value. Use it when the fix lives in code, not CSS.
4. **mock-up** only when none of these can show it (a screen that doesn't exist). Label it "mock-up" on the page.

Try a candidate value, measure (count hidden labels, check contrast), and adjust before settling. Note the files and lines the real fix would touch: they go in each finding's `where`.

## Page contract

Fill `template.html`'s `FINDINGS`, `ASKS` and header fields. Keep its structure; it's built so every review reads the same.

- **Header.** Project name, build (commit), viewports and scale, data state (seed, defaults), the rules version, the date. A tally of Off, Ask and Try.
- **Read and Squint.** The full desktop capture with numbered read-order markers placed on what reads 1st, 2nd, 3rd, and a dashed `?` on what should read first but doesn't. A "Squint at it" toggle blurs the capture.
- **Off.** One card per finding: rule chips, a short title, the visible fact, what it costs, the fix, where it lives in code, and a before/after pair. Clicking either picture opens a modal with a drag-to-compare slider. Three buttons: **Fix it**, **Not now**, **It's on purpose**.
- **Ask.** One card per question: why it's a question, two or three rendered options to pick, a "View larger" modal per option, and a free-text note.
- **Try.** All the Off fixes together, as an inline drag-to-compare against the before.
- **Working.** One specific strength, with a crop that shows it. List its rule IDs in `WORKING_RULES`.
- **Principles applied.** A card for each rule the review used, with the principle in one line and links to the Off, Ask and Working items that rest on it, then one line naming the rules walked with nothing to flag. It's built from the template's `RULES` list: add the repo's `.claude/squint.md` rules to it.
- **Footer.** How it was made (what was injected, what was computed) and how to answer.

Interactive detail opens in modals over the page (`<dialog>`), so the page stays readable as a sheet.

## Picks

Publish with `capabilities: {db: {}}`. The page writes one document per item to the `picks` collection: `{kind: "off" | "ask", choice, note, at}`. Choices: `fix`, `later`, `on-purpose` for Off; the option's value for Ask. Without `db` it falls back to browser storage and asks the user to say their picks in chat.

After publishing, `ArtifactData list picks` once: it should be empty. When the user says to apply the picks, read the collection again and act on it (see SKILL.md, "After the user picks").

## Gotchas

- Pages built on a canvas (3D, maps, charts) re-render on resize. Don't change the viewport between before and after.
- Moving a control in a fix may reflow a panel. Re-check that the clip still frames the same rows.
- A label system that hides collisions makes "missing" content invisible. Check it in the DOM, not the picture.
- Image `loading="lazy"` leaves full-page screenshots blank. The template doesn't use it.
- Every `<img>` carries `width` and `height` (no layout jump) and CSS `height: auto`. Without `height: auto`, a CSS width plus the `height` attribute stretches the picture.
