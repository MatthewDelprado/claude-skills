---
name: close-out
description: End-of-session cleanup for any repo. Writes a session summary, commits and pushes only this session's work, audits stale references and docs, checks verification coverage, tidies GitHub issues, and proposes improvements to itself. A repo's `.claude/close-out.md` overrides the defaults; the first run interviews you to create it. Trigger on "close out", "wrap up", "let's close this off", "clean up after this", or "close-out setup".
---

# close-out

Leave the repo so a future agent starting cold can see what was built and why, nothing is half-done, and whatever watches the repo will catch drift. Work through the steps in order; surface issues one at a time, not as a dump.

**Defaults, then overrides.** Every step states a universal default. A section in the repo's `.claude/close-out.md` replaces the matching default; anything it doesn't mention keeps it. If config and this file conflict, config wins for that repo. Repo knowledge is read from the config, never assumed here.

`close-out [MODE=run|setup]`: `run` (default) for "close out", "wrap up", "let's close this off", "clean up after this"; `setup` for "close-out setup", "reconfigure close-out" (re-runs the interview against the existing config). `whats-next` hands off here when a session is done.

## Command shape

Run shell commands one at a time, each a single static command: no `$(...)` or backticks, no `cd <dir> && …` chained with a pipe or redirect, no values computed inline. Those shapes can never get a durable allow rule and stall unattended runs on a permission prompt. Read each result, do any arithmetic or comparison yourself, then write the next command with literals. Prefer Read, Grep and Glob over `cat`, `grep`, `ls`.

For `gh`, always pass `--repo <owner>/<repo>` as a literal, taken from the config's `## Issues`; failing that, run `gh repo view --json nameWithOwner` once on its own and reuse it. Snippets below are shapes with `<placeholders>` to fill in.

**Session title.** If the `rename-session` skill is installed, call it first (`STATE=closing`, before the summary) and last, once everything has landed (`STATE=done`, `STATE=parked WHEN=<date>` or `STATE=waiting NEED=<what>`). Skip silently if absent.

## Find the config

Look for `.claude/close-out.md` in the current directory, then at the repo root (`git rev-parse --show-toplevel`, on its own). Use Read or Glob.

- **Found** → read it. Every section is optional.
- **Redirect:** if the whole file is `redirect: <path>` (relative to it), follow it and treat the target's repo as the root for everything below.
- **Not found**, or `MODE=setup` → read `setup.md` in this skill's directory and follow it, then continue into the run.
- **Not a git repo** → skip the git steps (1, and 7's commit); say so once.

## Externally visible writes may be denied

Step 1's push, Step 5's issue create/comment/close, Step 7's landing and any Extra step that merges a PR are writes the harness's auto-mode classifier may deny, even when CLAUDE.md or this skill authorizes them; invoking close-out doesn't authorize a *specific* external mutation. When one is denied:

- Don't work around it: no rephrased retry, alternate tool, or API call doing the same thing.
- Put the exact content (comment text, issue title and body, commit range to push, merge decision with evidence) in the closing report for the user to approve or post.
- If the repo has its own automation for the write (e.g. auto-merge), say so and let it pick the change up.
- Carry on with the other steps. Don't file a Step 6 proposal for the denial itself; it's a known theme.

## Parked sessions

If the user will come back on a date (says so, or the follow-up is a check at a known time), read `parked.md` in this skill's directory before Step 0 and add its extras to every step.

## Step 0 — Session summary

**Default:** write `sessions/YYYY-MM-DD-<slug>.md` before anything else; slug is 2–4 words (e.g. `zero-token-polling-architecture`). Get today's date from a fresh `date` call, since a long session can cross midnight.

**Overrides** (config `## Session summary`):
- `Path:` a different location, or `none` to skip the file.
- `Log:` the repo keeps a running log instead of or as well. After Step 1, append one headline line per meaningful change in the log's own format, citing the real commit hash: commit the work, read the hash, append, then commit the log in a small follow-up. The log holds the headline; git holds the detail.

The summary is how a future agent learns why decisions were made, so write for someone with no memory of this conversation:

```markdown
# <Title> — YYYY-MM-DD

## What was built
[Concrete deliverables: scripts, skills, config files, jobs]

## Why
[The reasoning, trade-offs, rejected alternatives. The part git history doesn't capture.]

## What was retired
[Anything deleted, disabled or replaced, and what replaced it]

## Key decisions
[Hard, surprising or notable decisions. Link ADRs if any.]

## Follow-up
[Open issues filed, deferred work, known gaps]
```

The config may add sections or require headings verbatim (tools sometimes parse them). If the conversation covered two or more unrelated threads, write one file per thread with its own slug; if they share decisions, one file with H2 sections is fine. Be specific (exact files, exact reasoning, exact trade-off); a small session gets a short summary.

## Step 1 — Git hygiene

Run `git status` and `git diff --stat` (read the stat: a few intended lines reporting hundreds of deletions is a bad scripted edit, not a big one; `git checkout -- <path>` is free before staging, expensive after pushing).

**Assume the tree is not quiescent.** Parallel sessions and scheduled runs may be writing to it, and committing their work under this session's message corrupts the record close-out protects.

- Stage and commit **only paths this session touched**, by name. Never `git add -A` or `git commit -a`. Re-run `git status` right before committing.
- **Pass the pathspec to `git commit` itself** (`git commit <files> -m "..."`) so nothing sits in the index for another session's bare commit to absorb. A new file needs an `add` first; chain them: `git add <new> && git commit <new> <changed> -m "..."`.
- **A hot shared file another session is editing right now** (index, registry, changelog, log): `git commit <path>` commits the whole working-tree content, foreign hunks included. Run `git diff <path>` first and confirm every hunk is yours. If not, stage only your hunks (`git add -p`, or `git apply --cached` with a patch of just them), check `git diff --cached --stat` shows nothing else, then run a bare `git commit`.
- One commit per coherent change, not per file. Untracked files you own: meaningful (scripts, config, docs) → commit; noise (temp, runtime state, backups) → `.gitignore` or delete. An untracked directory is someone else's unless you created it.
- Prefer exact string replacement with a per-site assertion over a regex for scripted edits; never a `DOTALL`/multi-line pattern across a code fence.
- **Changes this session didn't make.** Default, unless config `## Git` sets a policy for that path:
  - Another session's or a job's work (different topic, files a running job writes, a directory you didn't create) → leave uncommitted, name it in the report.
  - The user's hand edits → only for paths the config lists under `Hand-edited paths:` with `policy: commit separately`: commit them in a **separate** commit labelled as swept-in edits and list them as an FYI. Without that line, a dirty file can't be told from another session's WIP, so don't sweep it in.
  - High-blast-radius files (schema, CI config, `CLAUDE.md`/agent instructions, shared settings) the session never discussed → show the diff and ask. They must never ride along silently.
  - Anything else → leave uncommitted and name it. Sweeping in half-done work and pushing it is worse than leaving a file dirty.
- Run whatever config `## Git` adds.
- Push per the config's policy (default: push the current branch if it has an upstream; never force-push). Expect to pull/rebase. Another writer may already have pushed this session's commits (`git log --oneline HEAD@{1}..HEAD` or `git status -sb`); if so, say that rather than reporting a push you didn't make. Work deliberately held unpushed belongs on a branch. If the session ran on a temporary worktree branch, say so in the report; work left only there is easy to strand.

Report what was committed, what was ignored, and what was deliberately left uncommitted and why.

## Step 2 — Stale reference audit

From git log, recent changes and the conversation, list what this work **retired, renamed, replaced or reconfigured** (a changed value can leave live docs wrong like a changed name). Propose the list before grepping: "I think these were retired or changed: [list]. Anything to add or remove?" Then search the repo for each term (Grep, or one plain `grep -rn "<term>" .` per term).

Two more passes a rename grep misses:
- **Disproven beliefs.** Did this session overturn something the repo recorded as true? Grep the claim's distinctive terms (numbers, mechanism, symptom name), not file names, and check any index or routing table first; a stale row there sends the next investigation down the disproven path.
- **Superseded practices.** If this session introduced a wrapper, helper or guardrail, grep for the *old shape* (raw command, direct API call, manual append). Convert remaining callers or file an issue with the exact count; a guardrail nothing routes through reads as coverage but isn't.

Classify each hit:
- **Historical** (migration doc, changelog, git log, past session notes) → leave.
- **Live instruction or reference** (a skill fallback, a docs table, a README) → update to current state. Judge by phrasing, not heading: if a future agent could act on the sentence (`Fix:`, "always", "never", "run this") it's live, even in a post-mortem or `REJECTED:` section. If it was right at the time, supersede in place with a dated note rather than delete.
- **Generated or mirrored** (config's audit section names these) → edit the source and let the mirror regenerate; a direct edit is silently reverted.

Then run config `## Stale-reference audit` items. For flag-only ones, report drift and reconcile by hand; don't blind-copy.

Also find scripts, jobs or files that were replaced but sit on disk uncalled. Delete them now, unless the session summary's Follow-up or "What was retired" names the file *and* the reason to keep it (e.g. "safety net for a week, delete next close-out").

Report what was updated, deleted, and intentionally left.

## Step 3 — Documentation currency

Check the docs in config `## Docs`. With no table, check whichever of `README`, `CONTEXT.md`, `ARCHITECTURE.md`, `docs/` and ADRs describe what changed. If the repo keeps ADRs and this session made a hard-to-reverse, surprising decision with a real trade-off, offer to write one. Fix only what drifted; don't rewrite.

## Step 4 — Verification coverage and gates

For each new piece of infrastructure or behavior, ask: **would anything notice if it broke or drifted?** (a test, CI, a monitor, a health check). The question misses three cases:

- **Changed parameter on existing infrastructure** (model tier, schedule, timeout, delivery target): nothing new was built, so nothing prompts a check. Find the existing guard for that mechanism and run it against the new value.
- **Component added to a shared mechanism** (a check in a runner, a job in a dispatcher, a row in a registry): read its iteration path and see what it does with a component that is present but unusable (not executable, malformed, throwing). If it skips in silence, every addition is a possible silent no-op. Say in the report which mechanism you extended and what it does on a bad component.
- **A claim that an entry was added** ("added Check N", "added row X"), yours or a prior session's, is unverified until the id or key is confirmed in the live file. Grep it; report a claimed addition that is missing.

If the session fixed a bug, make sure verification exists: a test now, or an issue with explicit success criteria if it can't be verified yet. Propose a concrete addition only where a real failure would otherwise be silent; no speculative checks.

Then run config `## Gates`, each when its **When** applies. **stop**: halt on failure, say what failed, continue only when resolved or the user overrides. **ask**: show the result and wait. **warn**: note it in the report and continue. With no gates, this step is the coverage question only.

## Step 5 — Issues

Skip if the config names no tracker and `gh` isn't usable.

```bash
gh issue list --repo <owner>/<repo> --state open
```

- Issue now resolved by this work → close it with a note.
- Follow-ups not yet captured → file issues, each self-contained for a reader without this conversation.
- **Claimed issues:** for any issue this session marked in-progress, remove that label and comment what happened, whether closed or left open. The label means "someone is actively on this right now", not "unresolved".

**Labeling gate (every issue filed this session).** Copy the convention in the config or from 2–3 recent issues; don't invent labels. If its labels don't exist, create them first (`gh label create "<name>" --repo <owner>/<repo> --force`, one each). Triage sweeps by label, so an unlabeled issue is invisible to it. Check each filed issue and apply the labels to any with an empty list:

```bash
gh issue view <n> --repo <owner>/<repo> --json labels
```

**Comment-currency gate (every issue this session commented on, closed, or referenced in a commit).** A long session posts an update partway and keeps working, so check each issue's last comment is still the last word. Run these two on their own:

```bash
gh issue view <n> --repo <owner>/<repo> --json comments --jq '(.comments[-1].createdAt // "1970-01-01T00:00:00Z") | fromdate'
git log --grep="#<n>" --format="%ct" -1
```

Both print Unix epochs; compare the numbers directly (never `%cI` against `gh`'s UTC strings). Flag the issue if the commit's is larger. No comments counts as epoch 0; no `git log` output means nothing to compare. This flags candidates only, since `--grep` also matches a later commit that merely namechecks the number. For each flag, read the last comment and ask whether anything since changes what a reader needs to know. If yes, post a wrap-up comment; if no, leave it.

## Step 6 — Self-improvement

Read this file and reflect: was there a category of cleanup no step covers, a step too vague to execute precisely, or a step unnecessary for this kind of work? Route each finding:

- **About the flow** (any repo) → a proposal in the skill's source repo (the `repository` in the plugin's `.claude-plugin/plugin.json`), in `skills/close-out/IMPROVEMENTS.md`. **Don't edit this SKILL.md directly**: it's shared across repos and an installed plugin copy is overwritten on update. Surface the proposal to the user first; the source repo usually isn't the current one, so draft the entry and write and commit it in a clone only if the user says so.
- **About this repo** (a gate to add, a doc to track) → propose a diff to `.claude/close-out.md`; apply it after the user approves.

**Dedupe before writing.** Repetition in a proposals file means a theme was missed. Grep the file's `## ` headings (case-insensitive) for 2–3 keywords of your theme. 0 matches → write the proposal. 1–2 → append your evidence (date, what happened, commit SHA) to the existing entry. 3+ → stop proposing; file a GitHub issue with the recurrence count and links to every prior entry, and add one line to the existing entry pointing at it.

## Step 7 — Land what close-out changed

Steps 2–6 edit things after Step 1's commit (doc fixes, config, the run log). Land them so the session doesn't end on a dirty tree:

1. Run config `## Run log` command, if any.
2. Commit exactly the paths steps 2–6 and the run log touched (Step 1 pathspec rule); push per policy.
3. `git status` should show none of *your* paths; other sessions' changes aren't yours.

**Closing report.** Default: a short scannable summary of what was committed (real hashes), issues opened or closed (real numbers), anything needing the user's call, and what was deliberately left uncommitted. Use config `## Closing message`'s format if it gives one. If a write was denied or failed, say what landed and what didn't; never report success you didn't confirm.

Unless the session is parked (`parked.md` banner), end with exactly this as the final message (or the config's `Banner:`):

```
---------------------------------
Session is now closed out
---------------------------------
```
