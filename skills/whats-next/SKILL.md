---
name: whats-next
description: Walk the user through the remaining work in a session one step or decision at a time — short prompts they can answer in a word or two, each with a recommended default. Like a grilling session, but for finishing rather than designing. Ends only when the session is blocked on something hours away, or is done and ready to close out. Trigger on "what's next", "whats next", "what's left", "step me through the rest", "walk me through what's remaining", "one at a time until we're done".
---

# What's Next

Turn the remaining work in a session into a queue, and walk the user down it one prompt per turn. They should be able to reply in a word without losing the thread.

This is the finishing counterpart to a design grilling. A grilling resolves a decision tree to design something; `whats-next` resolves the leftovers to *ship* something.

Works in any repo. Optional companions, used only if installed: `rename-session` (session title) and `close-out` (end-of-session cleanup).

---

## Interface

`whats-next [SCOPE=session]`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| SCOPE | string | `session` | `session` = everything still open in this conversation. Any other value narrows to that topic or project (e.g. `SCOPE="retry policy"`). `all` widens past this session. |

**Parse from natural language:**

| User says | Params |
|---|---|
| "what's next" · "what's left" · "step me through it" | `SCOPE=session` |
| "what's left on the retry policy stuff" | `SCOPE="retry policy"` |
| "what's next across everything" | `SCOPE=all` — widen past this session: open GitHub issues, plus any task list or notes file the repo keeps |

**Skill-to-skill:** a planning, grilling or feature skill can hand off with `whats-next SCOPE="<topic>"` once design is settled and only execution remains.

---

## 0. Retitle the session — first act

If the `rename-session` skill is installed, run it (auto) before building the queue. Work is resuming, so this drops any `Needs you:` / wake-date prefix and sets the mode to what's being finished. Silent; no report line. Skip if it isn't installed.

## 1. Build the queue — don't ask for it

Derive it yourself, silently, before the first prompt. Sources, in order:

- What actually happened in this session: things started and not finished, "we'll do that after", "leave that for now", unanswered questions you asked, decisions deferred.
- Anything you changed that isn't committed, verified, or registered.
- If `SCOPE` is a topic: the relevant code, docs, open GitHub issues and state files for it.
- If `SCOPE=all`: `gh issue list --state open`, plus any task list or notes file the repo keeps.

**Never ask the user a question you can answer with a lookup.** Read the file, run the `gh` query, check the state. A question that a `grep` would have settled is a wasted turn.

Then order it:

1. **Blockers first** — anything that gates other items.
2. **Then user-only items** — decisions, approvals, physical-world checks, things only they know.
3. **Then long-lead items** — anything that starts a clock (a deploy to soak, a job to fire, a reply to wait on). Start these early so the waiting overlaps the rest of the session.
4. **Anything you can just do, you do** — don't put it in the queue as a question. Do it, report it in one line, move on.

---

## 2. The rhythm — one prompt per turn

Each turn is **one** step or decision. Shape:

- One line of context, only if it isn't obvious.
- The ask, in plain language.
- A recommended default, marked as such.
- If it's a decision, 2–4 short lettered options so they can reply "b".

Under five lines. No preamble, no re-listing the queue every turn, no progress bar, no "great question". Terse is the point — they're answering fast.

After their reply: **act on it and move to the next item in the same turn.** Don't ask permission to continue. Don't summarise what you just did in more words than it took to do.

Show position only when it's genuinely useful — roughly every fourth turn, or when the queue changes size — as a short tail like `(3 left)`.

---

## 3. Re-derive between turns

Their answer can add items, kill items, or reorder everything. Rebuild the queue after each turn rather than marching a stale list. If the shape changed materially, say so in one line before the next prompt.

---

## 4. Breaking the rhythm — expected, not a failure

The one-per-turn cadence is a default, not a cage. Break it whenever one of these is true, say in one line that you're breaking it, do the thing properly, then return to the cadence.

| Trigger | What to do instead |
|---|---|
| The next item is **work, not a question** | Just do it. Report in a sentence. Continue. |
| Their answer opens a **real decision tree** | Resolve that branch properly, one question at a time with a recommended answer, then resume the queue. For a genuinely contested call, lay out the strongest case for each side before recommending. |
| They **ask a question or raise something new** | Answer it properly at full length. Absorb it into the queue. Resume. |
| They **can't answer without an explanation** | Give the explanation — short, one default path, say what differs before an "or" — then ask. |
| You find something that **contradicts the queue** | Stop, rebuild the queue, say what changed in one line. |
| The item is an **external or irreversible action** (outbound message, calendar delete, production change, force-push) | Full stop on the rhythm. Present the actual artefact in full — the draft, the diff, the exact command — and get explicit approval. Only after they've seen it does a one-word "yes" count. Never let the fast cadence carry a send through on a reflex reply. |
| They reply **"skip" / "not now" / "later"** | Park it silently, move on. If three in a row get parked, ask whether to stop here instead. |
| The queue turns out to be **one item** | Don't perform the ritual. Just say what the one thing is. |

---

## 5. Endpoints — there are only two

Keep going until one of these is true. Don't stop just because the queue feels long, and don't invent a third exit.

**A — Blocked and waiting.** Nothing left that can be done now; the next move depends on something hours away (a deploy soaking, someone's reply, a job firing, a physical check). Say what's blocked, on what, and when it's worth coming back. Offer to set the return trip with a reminder or scheduling tool if one is available; otherwise say plainly what to check and when. If the session is being kept open until then and `rename-session` is installed, rename it: blocked on something the user has to do → `rename-session STATE=waiting NEED=<what>`; blocked on time or someone else → `rename-session STATE=parked WHEN=<return date>`. Then stop.

**B — Done.** Nothing left. Say so plainly in one line, then decide whether this is the end of the session:

- **Clearly the end** — the queue is empty, nothing parked needs a decision, and the user hasn't signalled more work coming (they've answered the last item with "done", "that's it", "nope", or similar). Don't offer — **go straight into close-out** in the same turn: invoke the `close-out` skill if it's installed; if it isn't, commit and push this session's outstanding work. Say "Moving to close-out." and start.
- **Not clearly the end** — they've mentioned other work, the session drifted across topics that may still be live, or `SCOPE` was a narrow topic inside a bigger session. Ask once, recommended default first: "Close out now? (recommended) · or keep going on something else".

If you ask and they pick "keep going", run `rename-session` (auto) so the title names the new work. If close-out runs, it handles the title at both ends; don't rename here as well.

Close-out's own external-action gates (pushes, issue edits, outbound messages) still apply — moving into it automatically doesn't pre-approve anything it would normally confirm.

Either way, anything parked or unresolved goes somewhere durable before the session ends — a GitHub issue, a task, a note in the repo — not just in the transcript.

---

## 6. Anti-patterns

- Asking two things in one turn "since they're related".
- Asking what a lookup would answer.
- Re-listing the whole remaining queue each turn.
- Ending at "that's probably everything" without hitting endpoint A or B.
- Staying in cadence through something that deserved a real conversation.
- Long acknowledgements. "Done." is a complete turn.
- Offering close-out and waiting for a "yes" when the session is obviously over — just start it.
