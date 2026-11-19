# squint rules

The starting set. Each rule has a permanent ID: never renumber or reuse one. Retire a rule by marking it `(retired)` with the reason, rather than deleting it. New rules go under **Learned**, with the next unused ID and where they came from.

A repo's `.claude/squint.md` can add rules, switch rules off for that repo, or give its own values (its spacing scale, its type sizes). It wins over this file.

## Read

### S1 · One job
- Can you name the screen's job and its main action within a few seconds?
- Does every element help with that job? Name anything that pulls attention away from it.

### S2 · Squint order
- Blur your eyes. The loudest thing should be the most important thing.
- Is anything minor shouting (a badge, a border, a decorative image), or anything important fading?

## System

### S3 · Type
- Each piece of text has one role (title, body, label, value, metadata), styled the same way everywhere.
- Few sizes per screen. Before adding a size, try weight, colour or space.
- Body text runs at a comfortable line length (roughly 45–75 characters) with enough line height.

### S4 · Spacing
- Gaps come from a scale (for example, multiples of 4 or 8), not one-off values.
- Things that belong together sit closer than things that don't: tighter inside a group than between groups.
- Empty space looks placed on purpose, not left over.

### S5 · Alignment
- Edges share lines. A near miss (off by 1–3 px) looks worse than a clear difference.
- Repeated items line up across rows and columns.

### S6 · Colour roles
- Each colour does one job. The accent is kept for action and selection.
- Status colours (success, warning, error) mean only status.
- Neutrals are one temperature, with no near-duplicate greys.

### S7 · Shape
- Only a few corner radii. A nested corner is the outer radius minus the padding between them.
- Strokes share a width, and icons share a size and style.

### S8 · Depth
- Separate things with space first, then a surface tint, then a border, and a shadow last.
- Borders are as light as they can be and still work.
- Light and shadow agree on one direction.

### S9 · Optical fixes
- Where the maths is right but it looks wrong (an icon in a circle, a play triangle, text in a button, round shapes next to square ones), it's been corrected by eye.

## Use

### S10 · Actions
- One primary action per view, and clear tiers below it.
- Anything clickable looks clickable, and nothing static does.
- Destructive actions are deliberate and set apart from the happy path.

### S11 · States
- Hover, focus, pressed, disabled, loading, error, empty and overflow are designed, not left to default.
- The user can see what they did, that it's in progress, and how it turned out.

### S12 · Copy
- Buttons name the outcome ("Save changes", not "OK").
- Placeholders don't repeat the label. Errors say what to do next.
- Headings say what's here, not what the section is called internally.

### S13 · Real content
- It holds up with long names, missing data, one item and a thousand items, and longer translated text.
- Truncation and wrapping are designed, not accidental.

### S14 · Flow
- Count the steps and decisions between the user and their goal. What could go?
- Controls and chrome don't crowd out the content.
- A form asks only for what it needs, and a long flow shows progress.

## Access

### S15 · Contrast
- Body text at least 4.5:1, large text at least 3:1, and icons and borders people need to find at least 3:1 (WCAG AA).
- From a screenshot, these are estimates. Say so.

### S16 · Beyond colour
- No state relies on colour alone: it still reads in greyscale.
- Focus is visible.

### S17 · Size
- Tap targets at least 24 by 24 CSS px, and the platform minimum where there is one (44 pt on iOS, 48 dp on Android).
- Body text at a comfortable size for the platform (around 16 px on the web).

## Restraint

### S18 · Earn it
- What can be removed before anything is added?
- Every shadow, gradient, blur and effect has a job.
- A custom pattern where a standard one exists has to pay for itself every time someone uses it.

### S19 · Generated-UI tells
- Everything emphasised, so nothing is.
- Cards inside cards inside cards.
- Gradients, glows and badges added for decoration.
- Emoji standing in for icons, and filler copy.

### S20 · Motion
- Each animation explains a change: where something came from, went, or what caused what.
- Quick and calm in task flows. Everything still makes sense with reduced motion.

## Learned

Rules from the user's own calls land here, with the next unused ID and the issue they came from.
