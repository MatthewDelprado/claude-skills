---
name: show-me
description: Explain something visually, fast, right in the session. Picks the quickest visual that shows the shape of an idea (before→after, journey strip, concept map, option scorecard, 2×2, status board, sketch mockup, explainer) instead of writing prose. Sketches only, for the user in this session: no files, no publishing. Trigger on "show me" on its own, "/show-me", "show me how / why / what changed / where we are / the options / the flow / the difference / the big picture", "show me as a 2×2" (or any named format), "visualise this", "draw this", "diagram that". Not for "show me <a file, log, URL or command output>" — that just means display it.
---

# Show Me

The user wants to *see* something instead of reading about it. Draw the quickest visual that shows its shape, inline, now. This is a sketch for one person mid-conversation, not a deliverable: speed beats polish every time.

Works in any repo. Draws best in the Claude desktop app with the Mermaid Chart connector installed; without it, inline visuals and markdown cover everything, and in a plain terminal it falls back to text-only formats. Optional companion: `bro` (say it simpler, in words).

---

## Interface

`show-me [SUBJECT=last] [FORMAT=auto]`

| Param | Default | Description |
|---|---|---|
| SUBJECT | `last` | `last` = the previous assistant message. `topic` = the wider thread it belongs to. Anything else = that idea. |
| FORMAT | `auto` | `auto` = pick the best fit. A named format (`2x2`, `journey`, `table`, `before-after`…) = draw that, no choosing. |

**Parse from natural language:**

| User says | Params |
|---|---|
| "show me" · "/show-me" · "visualise that" | `SUBJECT=last` |
| "show me where we are" · "show me the big picture" | `SUBJECT=topic` |
| "show me how the checkout flow works" | `SUBJECT="checkout flow"` |
| "show me what this PR changes" | `SUBJECT=<the PR>`, conceptual before→after (see below) |
| "show me the options as a 2×2" | `SUBJECT=last`, `FORMAT=2x2` |

**This skill or plain display?** "Show me **X**" where X is a concrete thing you could open — a file, a log, an error, a URL, a command's output — means display it; don't use this skill. Where X is an idea, a relationship, a change, a flow or a set of options, it's this skill. When it's genuinely ambiguous, draw; the user will say "no, just the file".

---

## 1. Work out the subject

- **Default: my last message.** That's what the user was reading when they asked.
- **Step back when the last message alone won't draw.** If it was trivial ("done", "pushed"), or only makes sense with the context around it, visualise the wider topic instead. Judge it; don't ask.
- **"What changed" is conceptual.** For a PR, commit or edit, show what the thing did or was for before, what it does now, and why — never a diff tree or file list. If the conversation already explains the change (a PR description, your own summary), that's enough; read the diff only when it doesn't. Then draw the idea.

## 2. Know what you can draw with

Check once, from the tools you have:

| Tier | What | When |
|---|---|---|
| **1. Markdown** | Tables, box-drawing, indented trees, arrow strips (→), lanes for sequences | **Default.** Fastest; works everywhere, including a plain terminal. Simple flows and sequences go here too |
| **2. Inline visual** | A visual drawn in the chat by an app tool. Two kinds: the **Mermaid Chart connector** (tool `display_mermaid`, which may appear namespaced like `mcp__<id>__display_mermaid`), or the app's own inline-visual tool (in the Claude desktop app, `show_widget`) | When layout *is* the point and markdown would lose it |

**Which inline tool.** Mermaid when the shape is a graph it has a native type for: a flow or decision tree with branches, a sequence between actors, a concept map or entity relationships, a state machine, a timeline or roadmap. It lays out and routes the lines for you, so it beats hand-drawn SVG for those. `show_widget` for everything Mermaid can't place: 2×2s, mockups, fishbones, mini charts, scorecards with styling, what-ifs. A flow that fits a simple strip still goes in markdown (Tier 1).

**Mermaid is a connector, never raw text.** Without the connector it shows as code in the desktop app and a terminal, so never paste a ```` ```mermaid ```` block into the chat. Call `display_mermaid` with the diagram, once, for one sketch. If it asks for sign-in, say so in a line and draw in Tier 1 or `show_widget` meanwhile; don't stall. Use only `display_mermaid`: never `save_diagram`, `update_diagram`, or anything that stores the diagram in the user's account (see Out of scope). If it errors on syntax, one `repair_diagram` try is fine, then fall back.

**Connector missing: offer to install it, once.** Whenever show-me runs in the desktop app and no Mermaid tool is available, whatever the subject, draw the sketch first (Tier 1 or `show_widget`, never raw Mermaid), then offer the install in the same turn:

1. Call the registry's `search_mcp_registry` with `["mermaid"]` and pick the Mermaid Chart result.
2. If it isn't connected, call `suggest_connectors` with its `directoryUuid` and the keyword `diagrams`. That renders a Connect card; installing is the user's click, never yours.
3. Add one line under the sketch: `I drew this without Mermaid Chart; connect it with the card above and flows and sequences will draw properly next time.`

If the registry tools aren't available, give the one-line tip with the path instead (Settings > Connectors > Mermaid Chart). Offer once per session, and never again after the user ignores or declines. Not in a plain terminal (no connectors there). If the connector is installed but disabled for chat, say so in the line instead of suggesting an install. Once connected it may need a new session before `display_mermaid` appears; say so if the user asks again straight after connecting.

No inline-visual tool at all means you're in a plain terminal: use Tier 1 only. Never produce a format the place can't show.

**Before your first inline visual in a session, load the tool's guide** (for `show_widget`, call its `read_me` with the module that fits, e.g. `diagram` or `mockup`). Do it silently; don't mention it to the user. It's required, not polish: use only the classes and colour variables it defines, never invent variables or hard-code text colours, and make sure it reads in dark mode as well as light. **This skill decides *what* to draw; the guide decides *how*.** Where the guide nudges towards extras (clickable nodes, several diagrams, interactivity), keep it a single static sketch unless the format is a what-if. For Mermaid, keep the diagram to the same 3–7 elements, with short labels, and no custom styling beyond what makes the point.

## 3. Pick the format

Choose by the **shape of the question**, not the subject. A scorecard works for code approaches and design options alike.

| Question shape | Core formats | Also available |
|---|---|---|
| What changed / what's different? | **Before → after**: old vs new side by side, the shift highlighted | Current vs target (gap) |
| How does someone move through it? | **Journey strip**: 5–7 steps in a row, decisions and pain points marked · **Storyboard sketch**: 4–6 short text panels following one persona | |
| What's in it and how is it connected? | **Concept map**: things and the relationships between them | Sitemap / info architecture · Zoom levels (same system at 3 depths) |
| Which option? | **Scorecard**: 2–4 options × the criteria that decide it, with a pick · **2×2**: e.g. impact vs effort | Decision tree |
| Where are we? | **Status board**: done / doing / blocked / decided | Timeline / roadmap |
| What would it look like? | **Sketch mockup**: grey boxes and labels; 2–3 variants side by side when comparing · **Annotated screenshot**: only when a preview of the app is already running — capture it and add numbered callouts | |
| How does this work? | **Explainer**: the mechanism as labelled steps | What-if (toggles/sliders, inline visual only) · Analogy |
| Why did it happen? | | Fishbone (causes grouped by category) · 5 whys chain |
| What does the evidence say? | | Affinity clusters · Mini chart |

Core formats are the usual picks. Reach for the others only when the question clearly calls for one.

A named format skips choosing: draw that, even if it isn't in the table. If it isn't in the library, also offer to log it as a `missing-format` feedback item (step 7). If it can't work here (e.g. a what-if in a terminal), say so in a line and draw the nearest thing.

Sketch quality for everything: a journey is a strip, not a designed map; a storyboard is text panels, not illustrations. Keep roughly the 3–7 elements that carry the point.

On a 2×2 built from low / medium / high ratings, put mediums on or near the dividing line rather than forcing them into a quadrant. A format's standard framing (axis names, the usual quadrant names) isn't invented content, but prefer neutral names (Quick wins · Big bets · Fill-ins · Low value) over verdicts like "Avoid".

Keep table cells short — a few words. An option's one-off strength belongs in its column header or the pick line, not in a row of its own.

## 4. Draw it — and say little

- **Draw your best guess straight away.** No asking first.
- **One visual.** Pick the format that carries the point and draw it once. Don't follow a strip with a table of the same items; fold what the second one would add into the first.
- **Draw only what's there.** Every label, cell and placement comes from the subject. Leave a cell `—` rather than infer it; mark anything you had to assume `(assumed)` on the element itself. Choose the criteria or elements that decide the point, not ones that fill a grid. The same goes for any words around the visual: a "so what" line never adds a conclusion or dependency the subject doesn't state.
- **Name alternatives only on a genuine tie.** If two or three formats are about equally good, add one small line after the visual: `concept map · alt: before→after, scorecard`. If one format is obviously right, show just the visual.
- **Labels inside the visual do the explaining.** Text around it is a judgment call that leans small: often none, sometimes a line of "so what", longer only when the subject genuinely needs it. When you've stepped back to the wider topic, a short title saying so (e.g. **Migration: where we are**) is enough.

**Markdown sketches (Tier 1):**

- Keep lines under about 80 characters so they don't wrap in chat. If a strip won't fit, first merge minor steps or shorten labels, then wrap onto a second row with a `↓` turn. Put long notes under the step, not on the arrow line.
- Inside code blocks, use plain markers — `[!]`, `[x]`, `*`, `?` — not emoji, which are double-width and break alignment. Emoji are fine in tables.

Starting points:

```
Journey strip
Land ──→ Browse ──→ Add to cart ──→ [!] Sign-in wall ──→ Pay ──→ Done
                                    (drop-off here)

Journey strip, wrapped (turn down from the end of row 1, restart at the left)
Invite ──→ Set password ──→ Checklist ──→ [!] Import CSV
                                          (template not linked)
                                                 │
  ┌──────────────────────────────────────────────┘
  ↓
Pick template ──→ Schedule ──→ [!] Empty dashboard (up to a week)

Before → after
BEFORE  request → manual review (2 days) → approve → ship
AFTER   request → auto-check ─┬─ pass → ship
                              └─ fail → manual review
Shift: review only on failures

Sequence (lanes)
Browser              App server           Provider
   │── sign in ────────→│                    │
   │←─ redirect ────────│                    │
   │── consent ─────────────────────────────→│
   │←─ redirect + code ──────────────────────│
   │── code ───────────→│                    │
   │                    │── code→tokens ────→│
   │                    │←─ tokens ──────────│
   │←─ session cookie ──│                    │

2×2  (* marks the point; on the middle line = medium impact,
      on the centre column = medium effort, both = the crossing)
             low effort           high effort
         ┌────────────────────┬────────────────────┐
  high   │ Quick wins         │ Big bets           │
 impact  │  Bulk export       │  SSO               │
         ├────────────────────* Comments ──────────┤
  low    │ Fill-ins           │ Low value          │
 impact  │  Shortcuts         │                    │
         └────────────────────┴────────────────────┘
```

Status board — use only the rows that have items; rename or add rows to fit the work. Anything waiting on the user goes in **Your move** (with what it unblocks), not also in Blocked; Blocked is for things waiting on someone or something else:

| Status | Items |
|---|---|
| ✅ Done | … |
| 📌 Decided | … |
| 🔨 Doing | … |
| ⛔ Blocked | … (on what or whom) |
| 👉 Your move | … → unblocks … |
| ⏳ Later | … (not started or deferred) |

## 5. Iterate

Straight after a show-me visual, anything that means "change that visual" is a show-me follow-up — the user needn't repeat "show me". Typical moves, as examples rather than commands: *another way* · *as a <format>* · *simpler* (fewer elements) · *zoom in on X* · *zoom out* (wider context) · *bigger / make it nice*. Read intent, not phrasing.

"Another way" means a genuinely different format — the next-best from the same question-shape row, or from a neighbouring row that suits the subject — not the same format restyled. The alternatives line follows the same tie rule as a first draw.

"Bigger" or "make it nice": polished or shareable visuals are out of scope here. Say so in a line and offer the best sketch you can. (A separate skill for that may come later; once it exists, point to it.)

Further away from a show-me visual, those words mean whatever they normally would.

## 6. When nothing has a shape

Some things don't draw: a single fact, a yes/no, one instruction. First step back to the wider topic (step 1); it usually has a shape. If even that has nothing worth drawing, say so in a line. Give a plain-words version only if the original wasn't already plain; don't repeat an answer that was. If the trouble is that the message was hard to follow rather than shapeless, you may suggest `bro` if it's installed — suggesting is enough; don't call it.

## 7. Feedback → a GitHub issue

The feedback loop is how this skill improves. Failures only; never ask "was that useful?".

**When:**
- The user says it didn't work — "that didn't work", "bad visual", "show-me fail", "that's not helpful", or any equivalent, optionally with why.
- You can tell your own visual failed — e.g. the user replies "I just see code", or says the layout is broken.
- The user wanted a format that isn't in the library ("I wanted a Sankey and there wasn't one").

**Fix it first.** Before drafting anything, give the user what they wanted. After a render failure, redraw in Tier 1 — or Tier 2 if layout is the whole point (2×2, mockup, fishbone); after a Mermaid render failure, use `show_widget` or Tier 1, not Mermaid again — and don't reuse the format or tier that failed for the rest of the session. For a missing or wrong format, draw the one they asked for. Then draft the feedback below the fixed visual.

Wanted a format that's in the library but you picked another → `wrong-format`. Wanted one that isn't in the library at all → `missing-format`.

**Where:** always `MatthewDelprado/claude-skills`, whatever repo you're in.

**Scrub it.** The issue holds the *shape* of the failure, never the real content. Rewrite the ask with generic stand-ins ("show me how a checkout flow changed"). No company, client, product, team, people or repo names, no internal URLs or terms, no real data.

**Draft:**

```
Title: show-me: <format> <failure kind> — <generic one-liner>

**Ask (generic):** <the request, with stand-ins>
**Subject shape:** <e.g. a 6-step flow with one branch>
**Picked:** <format> · tier <1/2/other> · <why it was picked>
**Alternatives considered:** <or "none — it looked obvious">
**What went wrong:** <the user's words, scrubbed>
**Fix offered:** <format · tier> · user confirmed it worked: <yes / not yet>
**Minimal repro:** <a small fake example that shows the failure>
**Where:** <desktop app / plain terminal> · <date>
```

Record only what you've actually seen; write `unknown` for details of the failed turn you can't recall, and never claim the fix worked before the user has said so.

**Labels** (new issues only; comments don't take labels): `show-me`, `format:<format>` (e.g. `format:2x2`, `format:journey`), and one failure kind: `didn't-render` · `wrong-format` · `unclear` · `too-slow` · `missing-format`. `format:` is the format you drew — except for `wrong-format` and `missing-format`, where it's the format the user *wanted* and what you drew goes in **Picked**. Create only labels that don't exist yet (check with `gh label list --repo MatthewDelprado/claude-skills`, then `gh label create`); never overwrite existing ones. Quote label names in `gh` commands (`--label "didn't-render"`).

**Duplicates:** first search open issues labelled `show-me` with the same failure kind and the same `format:` (by the rule above; for `missing-format`, match the wanted format in the title too, since its label may be new). If one exists, the new incident becomes a comment on it (same template, no title), so repeats stack up as evidence.

**Preview — hard rule.** Run the read-only checks (visibility, duplicates, existing labels) first, then show the user the draft exactly as it will post (same line breaks), with the labels and whether it will be a new issue or a comment on #N listed outside it. Create labels and post only after the yes. Check `gh repo view MatthewDelprado/claude-skills --json visibility`; if the repo is public, say so in the preview. Post only after an explicit yes. Then give the link in one line and carry on.

Without `gh`, or without access, show the draft for the user to file by hand.

---

## Out of scope

- Polished, shareable or persistent visuals: no files written, nothing published, no outside canvases (whiteboards, design tools, docs). That includes saving a diagram to a Mermaid account: `display_mermaid` only.
- Code-review formats: diff trees, file lists, call stacks for review.
- Visualising unprompted. This skill runs only when asked.
