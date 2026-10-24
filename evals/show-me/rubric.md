# show-me grading rubric

Grade each case against the **general checks** plus its **case checks**. Each check is PASS / FAIL / PARTIAL with a one-line reason. Then give the case an overall score:

- **3 — good:** all MUST checks pass; the visual would genuinely help a busy person get the point faster than prose.
- **2 — acceptable:** all MUST checks pass, but it's clunky, over-long, or a weaker format than it should be.
- **1 — poor:** a MUST check fails, or the visual doesn't help.
- **0 — broken:** wrong behaviour entirely (e.g. drew when it shouldn't, posted without consent, leaked a confidential name).

## General checks (every case where the skill should run)

| ID | Check |
|---|---|
| G1 | MUST: Draws straight away — doesn't ask a clarifying question first. |
| G2 | MUST: Sketch, not deliverable — writes no files, publishes nothing, uses no outside canvas. |
| G3 | MUST: Uses only tiers the environment can show: never raw Mermaid text in the chat (it shows as code), Mermaid only through the connector's `display_mermaid`, and no inline visual in a plain terminal. |
| G4 | Format fits the *shape of the question*, and is one of the library's core formats unless the case clearly calls for another. |
| G5 | Text outside the visual leans minimal: none or a line or two, unless the subject genuinely needs more. No preamble like "Here's a visual of…" padding. |
| G6 | Alternatives line appears only when formats are genuinely close; absent when one format is obviously right. |
| G7 | Visual is legible: keeps the few elements that carry the point, labels do the explaining, alignment holds in a monospace font. |
| G8 | Tier choice is sensible: markdown by default, including flows and sequences; inline visual only when layout is the point. |
| G9 | One visual: doesn't draw the same items twice in two formats. |
| G10 | Draws only what's there: no invented cells, criteria, facts or causes; assumptions marked. |
| G11 | Markdown sketches stay under ~80 characters wide and use no emoji inside code blocks. Inline visuals load the tool's guide first and use only its theme variables, so they read in dark mode. |

## Case checks

**C01** — MUST: does *not* use the skill; simply displays the README (or offers to). Drawing a diagram = 0.

**C02** — MUST: does *not* draw; shows the error/stack trace. Drawing = 0.

**C03** — MUST: journey strip or flow of the onboarding steps (invite → password → checklist → CSV import → template → schedule → empty dashboard). MUST: marks the CSV-import stall (and ideally the week-long empty dashboard) as pain points. Markdown expected.

**C04** — MUST: recognises "Pushed." is trivial and steps back to the migration. MUST: shows the 5 steps with status (done / in progress 60% / blocked on backfill / not started, needs Priya's sign-off). Status board or progress strip both fine.

**C05** — MUST: scorecard (options × criteria) with Redis marked as the pick. SHOULD: criteria drawn from the message (hit rate, infra, invalidation, fit for per-user responses). No alternatives line expected (scorecard is obvious).

**C06** — MUST: conceptual before→after of the approval flow (all claims → manager queue, vs. ≤$200 + receipt → rules check → auto-approve, else manager). MUST NOT be a diff tree or file list; file names at most as a footnote. SHOULD state the shift (wait removed for small claims).

**C07** — MUST: status board (or equivalent) covering decided (magic link, drop remember-me), done (email template, token endpoint), doing (rate limiting), blocked (e2e testing on verifying a test inbox — and that it's the user's action), deferred (SSO). SHOULD give the user's action (verify a test inbox) its own visible row or line, not a parenthesis.

**C08** — MUST: concept map (entities + labelled relationships) including Account, Person, Team, Project, Role, and the Admin override. Inline visual or a clear markdown/box-drawing map both acceptable; relationships (many-to-many person↔team, role granted to person *or* team) must be correct.

**C09** — MUST: 2×2 with impact × effort axes, all six features placed correctly (Bulk export = high/low quick win; SSO = high/high; Keyboard shortcuts = low/low; Dark mode = low/medium; Comment threads = medium/medium; Offline mode = medium/high). SHOULD use the inline-visual tool (layout is the point) and label the quadrants. Mediums may sit near the axes.

**C10** — MUST: no inline visual, no Mermaid (neither tool exists). MUST: a markdown/ASCII 2×2 grid with the six features placed correctly. Aligned in monospace.

**C11** — MUST: low-fidelity mockup of the Settings page showing the four existing sections and the new Pause toggle with the 1h/1d/1w picker, placed sensibly (Notifications area). Inline visual expected; grey boxes, not a polished design. MUST NOT write a file or start a dev server.

**C12** — MUST: explainer of the OAuth code flow with the actors (browser, app server, Google) and steps in order. Markdown sequence lanes, an inline sequence diagram, or a labelled-step strip are all fine; Mermaid is fine only via the connector; a pasted mermaid block fails G3. Must be correct: the server, not the browser, exchanges the code for tokens.

**C13** — MUST: doesn't force a pointless diagram. SHOULD: tries stepping back, finds no wider shape, says in a line that this doesn't draw well. Since the original answer was already plain, it should *not* repeat it. A tiny visual that genuinely adds something is PARTIAL, not FAIL.

**C14** — MUST: treats "try that a different way" as a show-me iteration without needing "show me". MUST: redraws in a *different* format (e.g. table of who-can-see-what, zoom levels, hierarchy tree) — not the same concept map restyled.

**C15** — MUST: says polished/shareable output is out of scope for show-me, in a line. MUST NOT publish, write files, post to Slack or create an artifact. SHOULD offer the best sketch it can (e.g. a tidied version that pastes well).

**C16** — MUST: recognises a didn't-render failure without the user saying "file an issue". MUST: drafts feedback with the template fields. MUST: scrubs every confidential name (Ledgerline, Acme) — any leak = 0. MUST: finds #12 and drafts a **comment** on #12, not a new issue. MUST: says the repo is public in the preview. MUST: waits for an explicit yes — no post. MUST: redraws the deploy flow first (markdown, or `show_widget`), not Mermaid again. SHOULD: the draft records the fix as offered, not as confirmed working.

**C17** — MUST: drafts a new issue labelled `show-me`, `format:sankey` (the wanted format), `missing-format` — not `wrong-format`, since Sankey isn't in the library. MUST: scrubs "Orbit" from the draft and every command. MUST: preview + wait for yes; no public warning (repo is private). MUST: label names quoted in `gh` commands; only missing labels created. SHOULD: draws the Sankey now (inline visual) using exactly the given numbers (1,000 → 800 → 600 → 510, with the 200 / 200 / 90 drop-offs, and the 120 mobile non-openers only if shown as part of the 200) — any other number fails G10. SHOULD: puts the journey strip in **Picked** and records the Sankey as offered, not confirmed.

**C18** — MUST: treats this as the skill (an idea — how checkout works), not as "display checkout.ts". MUST: shows the 6-stage pipeline in order. Markdown strip expected.

**C19** — MUST: draws the flow once via `display_mermaid` (not a pasted code block, not also in markdown). MUST: no save/update of the diagram. SHOULD: 3–7 nodes, branch labelled, no install offer (connector present).

**C20** — MUST: draws the flow in markdown or `show_widget` (no Mermaid text). MUST: after drawing, calls `search_mcp_registry` then `suggest_connectors` for Mermaid Chart (the user clicks to install; no other install attempt) and adds one line under the sketch. SHOULD: line is brief, not a lecture. MUST NOT: repeat the offer later in the session.

**C21** — MUST: a 2×2 request with the connector missing still draws first, then makes the install offer (the offer is not limited to Mermaid-shaped subjects). MUST: the offer appears only once across C20-style follow-ups in the same session.
