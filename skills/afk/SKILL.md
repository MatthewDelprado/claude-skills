---
name: afk
description: Work unattended while the user is away. Never stop to ask: pick a recommended default and log it, or build several versions when the direction is unclear, and keep going until every remaining item truly needs the user. When the run ends, give a full report of what happened and walk the user through that run's open decisions one at a time, with a short catch-up before each one. Trigger only when the message asks to go afk: "afk", "/afk", "going afk", "work while I'm gone". Do not trigger on a mention of being away that isn't a request to keep working ("I'll be away Friday"), or on the word used in passing ("what does afk mean").
---

# afk

The user is leaving. Get as far as you can without them, then bring them back up to speed fast.

Works in any repo. A repo can override the hard lines below with `.claude/afk.md` (for example, to allow pushing work branches). Optional companions, used if installed: `rename-session`, `whats-next`, `close-out`.

## 0. Before they go: one message, no question

Send one short message, then start work without waiting:

- **Goal:** the outcome you're working toward, in one line. Take it from the user's message and the session so far. If neither gives a concrete task, don't go afk: say there's nothing to work on, and stop.
- **Log:** where the running log lives (see §2).
- **Hard lines:** what you won't do without them (see §3).
- **Prompt warning:** if the permission mode will stop on tool approvals, put this first and suggest switching to a mode that won't prompt before they leave. A prompt stalls the run just as a question would. Start anyway: an approval they find on return still lets the run continue.

If `rename-session` is installed, call `rename-session STATE=working`, and when you build the title, use `afk` as the mode segment.

## 1. Never ask, decide

From here until §5, don't ask the user anything and don't end your turn to wait for them. For each fork in the road:

| The choice is… | Do this |
|---|---|
| Answerable by looking (code, docs, issues, history) | Look it up. Never a question. |
| Reversible, or a sensible default exists | Pick the recommended option, log it as an **assumption**, carry on. |
| Shapes later work, and you can't tell what they'd want | **Build variants**: 2–3 versions side by side (a branch or worktree each for code, or `-a`/`-b`/`-c` files for docs and designs). Carry the main line on your pick and log it as a **decision** for their return. |
| Needs them (a credential, an approval, a physical check, a hard line) | Prepare everything up to the edge, log it as **queued**, and switch to other work. |

Standing instructions the user already gave (CLAUDE.md, memory, this repo's config) still apply, and they count as approval for what they cover.

Run independent work in parallel with subagents where available. While waiting on a long build or job, do other work. If nothing else is left, wait in the background rather than ending the turn, for up to an hour per wait. Past that, log it as **queued** (what it's waiting on) and leave it for the report.

Verify what you build (run it, test it). The report must say what's verified and what isn't.

## 2. Keep a log that survives

Context will be summarised on a long run. Keep a running log file so nothing gets lost: in the scratchpad if the session has one, otherwise `${TMPDIR:-/tmp}/afk/<topic>-<YYYY-MM-DD>.md`, in a folder only the user can read (`mkdir -m 700`). Append as you go, not at the end:

- **Done:** what changed, where it lives (branch, path, commit), and whether it's verified.
- **Assumption:** what you picked, what you didn't pick, and how to flip it.
- **Decision:** the open question, the variants and where each one lives, your pick.
- **Queued:** the exact command, draft or diff that's waiting for approval.
- **Dead end:** what you tried and why it failed, so nobody tries it again.

After any context summary, re-read the log and re-apply the `afk` rename before carrying on.

## 3. Hard lines while away

Unless `.claude/afk.md` or the user's standing instructions say otherwise (only an instruction that names pushing outright, such as "push work branches", overrides the first line), never do these while afk. Queue them instead:

- Push, merge, force-push, or open or merge a PR.
- Send, post or comment anywhere outward (messages, issues, PRs, email).
- Deploy, publish, or change production, accounts, settings or money.
- Delete anything you didn't create in this run.

The only exceptions are the two in §5: the push notification to the user and the private report page.

Local commits on a work branch are fine. If you're on `main` (or the default branch), create a work branch before the first commit, and keep the default branch untouched.

## 4. Exhausted means exhausted

Before stopping, take each blocked item through this ladder. Stop only when every remaining item fails all five:

1. Can a lookup settle it?
2. Can I pick a reversible default and carry on?
3. Can I build variants and let them choose later?
4. Can I stub, mock or fake the missing piece and carry on past it?
5. Is there other independent work toward the goal?

Don't stop because the work feels long, and don't stop to report part-way.

## 5. Coming back: the report, then the decisions

When you're truly out of options:

1. If a push-notification tool is available, send one line: "afk done: N decisions waiting".
2. If `rename-session` is installed: `rename-session STATE=waiting NEED="<N> afk decisions"`.
3. **The report.** Write the full report using `references/return-report.md`. If an Artifact tool can publish it as a page only the user can see (readable on a phone), do that. Never publish it anywhere shared or public: otherwise write it next to the log. Put the headline and the link in chat.
4. **The decisions, one per turn.** In the same message as the report, start the walk: the first decision, with its catch-up card from `references/return-report.md`. Order: blockers first, then decisions with variants, then queued actions, then any assumption worth a second look. After each answer, act on it (merge the chosen variant, delete the others, run the queued command once they've seen it), then show the next card.

Each card resets the context from scratch. Assume they remember nothing of this run, so don't say "as above".

When the walk is done, hand what's left to `whats-next` if it's installed, otherwise list it. If nothing is left, offer `close-out`.

## Anti-patterns

- Asking a question, or ending the turn to wait, before §5.
- Building variants for choices that don't matter. Pick and log them instead.
- More than three variants for one fork.
- A report that lists activity but not outcomes, or hides what isn't verified.
- Putting all the decisions in one message instead of one per turn.
- Treating a quick "yes" during the walk as approval for an outward action they haven't seen in full.
