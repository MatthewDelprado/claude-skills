---
name: council
description: Spawn parallel sub-agents to argue distinct positions on a hard decision, then judge between them and return a verdict. Trigger on "council", "/council", "council this", "get a council on X", "have them argue it out", or when the user says they are stuck on a hard choice and asks for the options to be argued out. Not for a routine either/or question, a plan to stress-test (grill-me), or remaining work to step through (whats-next).
---

## Interface

`council DECISION [POSITIONS=auto] [N=3]`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| DECISION | string | — | Required. The hard decision or question to resolve. |
| POSITIONS | string | `auto` | Optional. Comma-separated named options (e.g. "Job A, Job B, stay put"). If omitted, positions are auto-derived. |
| N | integer | `3` | Optional. Number of positions to auto-derive when POSITIONS is not given. Range 2–4. |

**Parse from natural language:** "council this: should I take the Sydney job or the remote one" → `DECISION="Sydney job vs remote job"`, `POSITIONS="Sydney job, remote job"`. "get a council on whether to rewrite the auth system" → `DECISION="rewrite auth system?"`, `POSITIONS=auto`.
**Skill-to-skill:** another skill can invoke with explicit `POSITIONS` to bypass auto-derivation.

## Is this actually a hard decision?

Before spawning anything, take one pass at the decision yourself. If one option obviously dominates and there's no real tension, say so directly in 1–2 sentences and stop — don't spawn a council for a no-brainer. Councils are for decisions that survive this first look.

## Step 1 — Frame the decision and establish the why

Restate what's actually being decided in one or two sentences. Then surface the motivation behind it: what outcome the user actually cares about, what's driving the ask now, what a good answer needs to satisfy. Skip straight to arguing positions without this and the council tends to litigate a generic, textbook version of the question instead of the one the user actually needs resolved.

- **Infer first.** Check the conversation so far, stated goals, and anything else already in hand. If a confident read is possible, state it in one line and move on — don't interrupt for something you already know.
- **Ask only if it would change the debate.** If the why is genuinely unclear, and different answers would point toward materially different positions or arguments, ask 1-3 targeted questions before spawning anyone (AskUserQuestion works well here; plain text is fine too). This is a pre-flight check, not a grill-me session — keep it to what's load-bearing.
- **Skip entirely when it's already explicit**, or when no plausible answer would change what the council should argue about.

If the decision as stated is too vague to argue at all (e.g. "should I change jobs" with no options in sight), fold that into the same question pass rather than treating it as a separate step.

Carry the established why forward — it's required context in every advocate's brief (Step 3), and the yardstick the judge (Step 4) weighs arguments against.

## Step 2 — Determine positions

- If `POSITIONS` is given explicitly, or the user's phrasing names the options, use those verbatim — one per advocate.
- Otherwise auto-derive `N` (default 3, range 2–4) distinct, mutually exclusive positions that represent the strongest real options — not the same option restated twice, not a straw man included just to be knocked down. "Do nothing / stay the course" is a legitimate position where relevant — don't drop it just because it's the least exciting one.

## Step 3 — Spawn advocates in parallel

Launch one Agent per position — all in a single message so they run concurrently — with `run_in_background: false` (the judging step needs every result before it can proceed). Do not let agents see each other's arguments; each argues blind, no cross-talk, no consensus-building.

Brief each agent with:
- The full decision context, plus the single position they've been assigned.
- The why established in Step 1 — advocates should make their case relevant to what the user actually cares about, not an abstract or textbook version of the trade-off.
- Their role: committed advocate, not neutral analyst. Build the strongest possible case for their position alone — not a balanced pro/con list.
- Ground claims in what they can actually verify (repo, web, memory) rather than assertion; flag inference vs. verified fact.
- Preemptively name and rebut the single strongest objection to their own position.
- Output format: one-line position statement, 3–5 best arguments with evidence, one rebuttal. Tight brief, not an essay.

## Step 4 — Judge

This is the part being delegated to you specifically — don't outsource it back to whichever brief sounds most confident. Read every brief critically:
- Weigh each argument against the established why first — a technically strong argument that doesn't actually serve what the user cares about should be discounted relative to a weaker-sounding one that hits the real motivation.
- Weigh evidence quality over persuasiveness. An unsupported confident claim loses to a weaker-sounding claim with a citation.
- Check each brief for exaggeration or unsupported claims and discount accordingly.
- Notice what's missing — did a brief ignore an obvious cost or risk of its own position?
- Form an independent verdict. You're not bound to pick the "winning" brief wholesale — synthesize a position none of them argued if the evidence points there, or declare a genuine toss-up if it is one.

## Step 5 — Report

- **Verdict** — the recommendation, one plain sentence.
- **Why** — 2–4 sentences of reasoning that references specific arguments from the briefs by name (credit or discredit them).
- **What would flip it** — the fact or condition that would change the verdict, so the user knows what to watch for.
- Keep the full advocate briefs available on request, but lead with the verdict — don't dump all of it into the main reply.

## Guardrails

- Cap at 4 positions — beyond that the judging step gets diluted and it's just burning tokens without adding signal.
- Floor at 2 positions — a one-agent "council" is an opinion, not a council.
- Synchronous and conversational only — nothing is written to memory or disk. If the user wants a record of the verdict kept, they'll say so.

## Related skills

- `grill-me` stress-tests one plan by interviewing the user. Use it when there is a single design to pin down rather than competing options to weigh.
