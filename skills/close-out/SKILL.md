---
name: close-out
description: End-of-session cleanup that works in any repo. Writes a session summary, commits and pushes this session's work without sweeping in other sessions', audits for stale references, checks docs and verification coverage, tidies GitHub issues, and proposes improvements to itself. Every step has a universal default; a repo's `.claude/close-out.md` overrides only what differs there, and the first run in a repo interviews you to create it. Trigger when the user says "close out", "wrap up", "let's close this off", "clean up after this", or "close-out setup".
---

# close-out

Structured close-out after a feature or session. The goal is to leave the repo so that a future agent starting cold can understand what was built and why, nothing is half-done, and whatever watches this repo will catch drift.

The flow is the same everywhere. What differs per repo — where summaries go, which docs must stay current, which checks gate the session, how issues are labeled — lives in that repo's **`.claude/close-out.md`**. If there isn't one yet, this skill interviews the user and writes it (see *First run in a repo*).

Work through each step in order. Surface issues one at a time — don't dump a list.

**Defaults, then overrides.** Every step below states a universal default. The repo's config can change any of them: a section in the config replaces the matching default, and anything the config doesn't mention keeps it. So a repo never has to restate the flow, only where it differs. If the config and this file conflict, the config wins for that repo. Nothing in this file is specific to one repo; if a step needs repo knowledge, it reads it from the config.

**Portability.** Ships as the `dp` plugin (or a symlink to its source repo), so it runs in any repo on any machine.

---

## Command shape

Run shell commands one at a time, each a single static command: no `$(...)` or backtick substitution, no `cd <dir> && …` chained with a pipe or redirect, and no values computed inline. Those shapes can never get a durable allow rule in Claude Code, so they stall unattended runs on a permission prompt. Read each result, do any arithmetic or comparison yourself, then write the next command with the values filled in as literals. Prefer the dedicated tools (Read, Grep, Glob) over `cat`, `grep` or `ls` where they do the job.

For `gh`, always pass `--repo <owner>/<repo>` as a literal. Take it from the config's `## Issues` section; failing that, run `gh repo view --json nameWithOwner` once, on its own, and reuse the answer. The snippets below are shapes to follow, with `<placeholders>` you fill in.

**Session title.** If the `rename-session` skill is installed, call it as the very first act (`rename-session STATE=closing`, before the summary) and as the last act, once everything has landed (`STATE=done`, `STATE=parked WHEN=<time>` or `STATE=waiting NEED=<what>`). Skip silently if it isn't there.

---

## Interface

`close-out [MODE=run]`

| Param | Default | Description |
|-------|---------|-------------|
| MODE | `run` | `run` = execute the close-out. `setup` = re-run the interview against the existing config and amend it (new CI, new docs, a gate that stopped earning its place). |

| User says | MODE |
|---|---|
| "close out" · "wrap up" · "let's close this off" · "clean up after this" | `run` |
| "close-out setup" · "reconfigure close-out" · "change what close-out does here" | `setup` |

`whats-next` hands off here when a session is done.

---

## Find the config

Look for `.claude/close-out.md` in the current directory first, then at the repo root (`git rev-parse --show-toplevel`, run on its own). Use Read or Glob, not a shell loop.

- **Found** → read it. Every section is optional; an omitted section means the default in the step below.
- **Redirect.** If the file's whole content is a line `redirect: <path>` (relative to that file), follow it and treat the target's repo as the root for everything below. This lets an umbrella directory that isn't itself a repo point at the repo where work actually happens.
- **Not found**, or `MODE=setup` → *First run in a repo*.
- **Not in a git repo** → git steps (1, 7's commit) are skipped; everything else still applies. Say so once.

---

## First run in a repo — the interview

One question per turn, each with a recommended default, answerable in a word. Not a form.

**1. Survey silently.** Read-only; never ask what a lookup answers.

- `CLAUDE.md`, `AGENTS.md`, `README`, `CONTRIBUTING` — stated conventions for commits, PRs, docs, memory
- Docs that describe the system: `CONTEXT.md`, `ARCHITECTURE.md`, `docs/`, ADRs, `CHANGELOG`
- Where handoff notes already live: `sessions/`, `notes/`, `docs/adr/`
- Checks: `.github/workflows`, and `package.json` / `Makefile` / `justfile` scripts for test, lint, typecheck, build
- Git: default branch, remote, whether recent history is merged PRs or direct pushes, worktrees or other signs of concurrent sessions
- Issues: `gh repo view`, `gh label list`, a few recent issues (labeling convention, any in-progress label)
- Duplicated or generated files (mirrors, copies of one doc, lockfiles) that drift; noise patterns in `.gitignore`

**2. Draft candidates.** For each close-out item the evidence supports, note what you found and a recommended default. Nothing found → no candidate. **Don't invent steps to fill a section**; a bare repo gets a minimal config (summary, commit, push) and you say so.

**3. Ask.** Start by offering the shortcut: "Found N candidate steps — walk through them, or start minimal?" Then, in this order and skipping anything with no evidence (except the two policy choices, which always get asked):

1. Session record — a summary file (default), a line in an existing log, both, or none. If the survey found a log the repo already keeps, recommend that *(policy)*
2. Push policy — direct to the default branch, PR, or don't push *(policy)*
3. Changes this session didn't make — only if the survey shows hand-edited content, or files with a big blast radius (schema, CI, agent instructions), worth naming as path classes
4. Docs that must stay current
5. Duplicated or generated files to reconcile
6. Gates — commands to run, and whether a failure stops the close-out, asks, or just warns
7. Issue tracker — repo, labeling convention, claim label
8. "Anything you always do at the end of a session here that I haven't listed?"

Aim for 8 questions or fewer. Record only what differs from the defaults in this file; a config that restates a default is noise that drifts.

**4. Write `.claude/close-out.md`** from the template below, show it in full, and continue into the run. It gets committed with the rest of the session's work.

### Config template

Omit any section that has nothing in it.

```markdown
# close-out config — <repo>

## Session summary
- Path: `<dir>/YYYY-MM-DD-<slug>.md`        (or: none)
- Log: `<file>`, one line per change, format `<line format>`   (optional; with Path: none, the log is the only record)
- Anything the default template must keep or add

## Git
- Branch and push policy
- Hand-edited paths: `<globs>` — policy: commit separately | leave | ask
- High-blast-radius paths: `<globs>` — policy: ask | commit | leave
- Shared-tree notes (concurrent sessions, files other agents own)
- Repo-specific hygiene commands

## Stale-reference audit
- Extra places to reconcile (mirrors, generated files, copies outside the repo), each with a command and whether to auto-fix or flag

## Docs
| File | Check |
|---|---|

## Gates
### <name>
- **When:** always | <trigger>
- **On fail:** stop | ask | warn
- command or question

## Issues
- Repo, claim label, labeling convention

## Extra steps
### After Step N — <title>
<instructions>

## Self-improvement
- Where repo-level proposals go

## Run log
- command, if the repo keeps one

## Skip
- Steps to omit, with the reason

## Closing message
- Report format: default | <template>
- Banner: default | <custom text>
```

---

## External writes may be denied by the auto-mode classifier

Applies to every step below that writes somewhere other people can see — Step 1's push, Step 5's issue create/comment/close, Step 7's landing, and any repo Extra step that merges a PR.

`git push` to a default/protected branch, `gh issue create`, `gh issue comment`/`close` and `gh pr merge` are external-visibility writes the harness's auto-mode classifier may deny, **even when the repo's own CLAUDE.md/AGENTS.md or this skill explicitly authorizes them**. Invoking `/close-out` is not itself user authorization for a *specific* external mutation.

When one is denied:
- **Do not work around it** — no retrying with a rephrased command, no alternate tool, no API call that does the same thing.
- **Draft the exact content** (comment text, issue title + body, the commit range to push, the merge decision and the evidence for it) and put it in the closing report for the user to approve or post themselves.
- If the repo has its own automated mechanism for the write (e.g. a GitHub Actions auto-merge workflow), say so and let it pick the change up instead of retrying by hand.
- Carry on with the remaining steps — one denied write doesn't stop the close-out.
- Don't write a new Step 6 proposal for the denial itself; it's a known theme, handled by this section.

---

## Parked sessions — close out now, come back on a date

Common case: the work is done for now, but there's a check at a known time (a soak, a week of real traffic, a reply). The user keeps the session open (not archived) and returns to it then. Treat it as parked when the user says so ("I'll check back on <date>", "don't archive") or when the follow-up is a check at a known time. A parked close-out runs every step as normal, plus:

1. **Return date.** Pin it as a weekday plus date and time ("Sat 17 Oct 10am"), never a relative word.
2. **Return brief in the summary.** Step 0's `## Follow-up` opens with a `**Return <when>:**` checklist of exactly what to check on return, with where to look (files, logs, commands). Someone who has forgotten the session should be able to start from it.
3. **Wake-up trigger.** Something must ping the user at the return time. Use the repo's reminder mechanism (config `## Parked sessions`), a scheduling tool if one is available, or say plainly that none exists. Put the session's `link` (from `mcp__ccd_session_mgmt__get_session`, `session_id: "self"`, when the desktop app tools are available) and the return checklist in the reminder text, so the ping leads straight back here.
4. **Issues.** Claimed issues still get their in-progress label removed (Step 5). The hand-off comment names the return date and what will be decided then.
5. **Compaction.** A parked session re-sends its whole transcript on every turn after the return, so a long one is expensive to resume. Claude can't compact the session itself, so the closing message ends with a ready-to-paste `/compact` line whose focus is the return brief, e.g. `/compact Keep only: return brief from sessions/<file>.md, open decisions, and what to check on <when>. Drop the investigation detail.` Leave this out for short sessions.
6. **Closing message.** Use the parked variant (Step 7).

## Step 0 — Write session summary

**Default:** before anything else, write a session summary file to `sessions/YYYY-MM-DD-<slug>.md`. Slug: 2–4 words describing the work (e.g. `zero-token-polling-architecture`).

**Overrides** (config `## Session summary`):
- `Path:` — a different location, or `none` to skip the file.
- `Log:` — the repo keeps a running log instead of (or as well as) summary files. Append one headline line per meaningful change in the log's own format, after Step 1 so the lines can cite the real commit hash. An accurate hash beats a single commit: commit the work, read the hash, append, then commit the log in a small follow-up. The log holds the headline; git holds the detail.

Use today's date from a fresh `date` call, not from memory: a long session can cross midnight.

The rest of this step describes the summary file.

This is the primary way a future agent understands why decisions were made — not git log, not commit messages. Write it for someone starting cold with no memory of this conversation.

```markdown
# <Title> — YYYY-MM-DD

## What was built
[Bullet list of concrete deliverables: new scripts, skills, config files, jobs]

## Why
[The reasoning that drove the work. Not what was done — why it was done this way
and not another way. Trade-offs considered and rejected alternatives.
This is the part git history doesn't capture well.]

## What was retired
[Anything deleted, disabled, or replaced — and what replaced it]

## Key decisions
[Decisions that were hard to reach, surprising, or worth calling out.
Link ADRs if any were written.]

## Follow-up
[Open issues filed, deferred work, known gaps]
```

The config may add sections or require headings to stay verbatim (tools sometimes parse them).

**Multi-thread sessions:** if the conversation covered two or more substantially unrelated chunks of work, write **separate files**, one per thread, each with its own slug. A future agent looking up "when did we last touch X" shouldn't have to skim a file mixing three topics. If the threads share decisions or trade-offs, one file with clear H2 sections is fine.

Be honest and specific. "Improved the system" is worthless; name the exact files, the exact reasoning, the exact trade-off. A small session gets a short summary, not a padded one.

---

## Step 1 — Git hygiene

```bash
git status
git diff --stat
```

**Assume the tree is not quiescent.** Other agents (parallel sessions, scheduled runs) may be writing to it, so at close-out the tree can hold modifications and untracked directories that belong to work still in progress elsewhere. Committing them under this session's message corrupts the record close-out exists to protect.

- Stage and commit **only the paths this session touched**, by name. Never `git add -A` or `git commit -a`.
- **Pass the pathspec to `git commit` itself** — `git commit <files> -m "..."` — so nothing sits in the index waiting for another session's bare `git commit` to absorb it. For a new file, which needs an `add` first, chain them in one command: `git add <new> && git commit <new> <changed> -m "..."`.
- **Pathspec discipline doesn't protect a file another session is also editing right now.** `git commit <path>` commits `<path>`'s whole working-tree content, foreign unstaged hunks included. Before committing a hot shared file (an index, registry, changelog or log that every session touches), run `git diff <path>` and confirm every hunk is yours. If a foreign hunk is there, don't pathspec-commit it: stage only your hunks (`git add -p <path>`, or `git apply --cached` with a patch of just your hunks), check `git diff --cached --stat` shows nothing else, then run a bare `git commit` so the index is what lands.
- Treat an untracked directory as someone else's unless you created it. Read `git diff --stat`, don't just run it: for a scripted multi-file edit, a few intended lines that report hundreds of deletions is a bad edit, not a big one (`git checkout -- <path>` is free before staging, expensive after pushing). Prefer exact string replacement with a per-site assertion over a regex, and never a `DOTALL`/multi-line pattern across a code fence. Re-run `git status` immediately before committing — the tree may have changed since you first looked.
- Group logically: one commit per coherent change, not one per file.
- Untracked files you own: meaningful (scripts, config, docs) → commit. Noise (temp files, runtime state, backups) → `.gitignore` or delete.
- **Changes this session didn't make.** Classify each, then apply the default unless the config's `## Git` sets a different policy for that path:
  - **Another session's or a scheduled job's work** (a different topic, files a running job writes, an untracked directory you didn't create) → leave it uncommitted and name it in the report. Never bundle it into this session's commits.
  - **The user's own hand edits** (content they edit directly, e.g. docs or notes changed in an editor outside the session) → commit them in a **separate** commit labelled as swept-in edits, and list them in the report as an FYI. Leaving them risks losing them, and a clean tree is the goal.
  - **High-blast-radius files** (schema, CI config, agent instructions such as `CLAUDE.md`, shared settings) that the session never discussed → show the diff and ask before committing. A stray edit there must never ride along silently.
  - **Can't tell which** → ask. Wrongly sweeping in another session's half-done work is worse than one extra question.
- Run whatever the config's `## Git` section adds.
- Push per the config's push policy (default: push the current branch if it has an upstream; never force-push). Expect to need a pull/rebase — the remote may have moved mid-run. Another writer, scheduled or interactive, may also have pushed this session's commits already (`git log --oneline HEAD@{1}..HEAD`, or check `git status -sb`); if so, say that rather than reporting a push you didn't make. Work deliberately held unpushed pending a decision belongs on a branch, not the default branch. If the session ran on a temporary worktree branch, say so in the report: work left only there is easy to strand. The config's push policy decides whether to land it on the default branch.

Report: what was committed, what was ignored, and **what was deliberately left uncommitted and why**.

---

## Step 2 — Stale reference audit

From context — git log, recent file changes, the conversation — identify what this work **retired, renamed, replaced, or reconfigured** (a changed value can leave live docs wrong just like a changed name). Propose the list to the user before grepping: "Based on what we built, I think these were retired or changed: [list]. Anything to add or remove?"

Then search the repo for those terms (the Grep tool, or one plain `grep -rn "<retired name>" .` per term).

Two more passes, because a rename grep misses them:

- **Disproven beliefs.** Did this session overturn something the repo recorded as true? Grep for the claim's distinctive terms (the numbers, the mechanism, the symptom name), not file names, and check any index or routing table first: a stale row there sends the next investigation down the disproven path.
- **Superseded practices.** If this session introduced a wrapper, helper or guardrail, grep for the *old shape* (the raw command, direct API call, manual append), not a name. Convert the remaining callers, or file an issue with the exact count. A guardrail nothing routes through reads as coverage but isn't.

Classify each hit:

- **Historical context** (migration doc, changelog, git log, past session notes) — leave it.
- **Live instruction or reference** (a fallback in a skill, a docs table, a README) — update it to the current state. Judge by phrasing, not heading: if a future agent could act on the sentence (`Fix:`, "always", "never", "run this"), it is live even inside a post-mortem or a `REJECTED:` section. If it was right at the time, supersede it in place with a dated note rather than deleting.
- **Generated or mirrored file** (the config's audit section names these) — stop; edit the source and let the mirror regenerate, since a direct edit is silently reverted.

Then run the config's `## Stale-reference audit` items. For anything the config marks flag-only, report drift and reconcile by hand — don't blind-copy.

Also look for scripts, jobs or files that were replaced but still sit on disk with nothing calling them; dead weight. **Carve-out:** a dead file is acceptable if the session summary's Follow-up or "What was retired" section names it *and* the reason to keep it (e.g. "safety net for the first week — delete next close-out"). Without that note, delete it now.

Report: what was updated, what was deleted, what was intentionally left.

---

## Step 3 — Documentation currency

Check the docs the config's `## Docs` table lists. With no table, check whichever of `README`, `CONTEXT.md`, `ARCHITECTURE.md`, `docs/` and ADRs describe what this session changed. If the repo keeps ADRs and this session made a hard-to-reverse, surprising decision with a real trade-off, offer to write one.

Update what has drifted. Keep changes tight — don't rewrite, just fix what's wrong.

---

## Step 4 — Verification coverage and gates

For each piece of new infrastructure or behavior this session built, ask: **would anything notice if it broke or drifted?** — a test, CI, a monitor, a health check. Three cases the question misses on its own:

- **Changed parameter on existing infrastructure** (model tier, schedule, timeout, delivery target). Nothing new was built, so nothing prompts a check. Look for an existing guard for that mechanism and run it against the new value.
- **Added a component to a shared mechanism** (a check to a runner, a job to a dispatcher, a row to a registry). Read its iteration path and ask what it does with a component that is present but unusable (not executable, malformed, throwing). If it skips in silence, every addition is a possible silent no-op. Say in the report which mechanism you extended and what it does on a bad component.
- **A claim that an entry was added** ("added Check N", "added row X"), yours or a prior session's, is unverified until the id or key is confirmed in the live file. Grep it. Report a claimed addition that is missing.

If the session fixed a bug, make sure verification exists: a test now, or an issue with explicit success criteria if it can't be verified yet. Propose a concrete addition only where a real failure mode would otherwise be silent; don't add speculative checks.

Then run the config's `## Gates`, each when its **When** applies:

- **stop** — on failure, halt the close-out. Say what failed and don't continue until it's resolved or the user explicitly overrides.
- **ask** — present the result and wait for a decision.
- **warn** — note it in the final report and continue.

With no gates in the config, this step is the coverage question only.

---

## Step 5 — Issues

Skip if the config names no tracker and `gh` isn't usable here. Get the repo as *Command shape* describes.

```bash
gh issue list --repo <owner>/<repo> --state open
```

- Any open issue now resolved by this work? Close it with a note.
- Follow-up items from this session not yet captured? File issues. Keep each self-contained — a future agent should understand the problem without this conversation.
- **Claimed issues.** For any issue this session marked as in-progress, remove that label and leave a comment summarizing what happened, whether it's closed or left open pending something. The label means "someone is actively on this right now", not "unresolved".

**Labeling gate — every issue filed this session.** Copy the convention in the config (or from 2–3 recently filed issues); don't invent labels. If the convention's labels don't exist yet, create them first (`gh label create "<name>" --repo <owner>/<repo> --force`, one per label). Automated triage typically sweeps by label, so an unlabeled issue is invisible to it. For each issue filed, check its labels:

```bash
gh issue view <n> --repo <owner>/<repo> --json labels
```

Any with an empty list → apply the repo's labels before finishing.

**Comment-currency gate — every issue this session commented on, closed, or referenced in a commit.** A long session posts an update partway through and keeps working; more commits land, other issues close, and the thread never gets a final pass. Before finishing, check whether each issue's last comment is actually the last word. For each issue, run these two on their own:

```bash
gh issue view <n> --repo <owner>/<repo> --json comments --jq '.comments[-1].createdAt'
git log --grep="#<n>" --format="%cI" -1
```

If the latest commit mentioning the issue is newer than its last comment, flag it for review. Compare the moments, not the strings: git's `%cI` carries a local offset (`+10:00`) while `gh` gives UTC `Z`, so convert both to UTC in your head before comparing.

**This flags candidates; it doesn't prove staleness.** `--grep` matches any commit *message* containing the number, including a later close-out commit that only namechecks it. For each flag, read the last comment and ask: *does anything that happened after it change what a reader needs to know?* If yes, post a wrap-up comment synthesizing what happened since. If no, leave it — a comment that adds nothing is its own noise. (It's also a known false-positive on sessions whose whole deliverable was issue comments; judge by hand.)

---

## Step 6 — Self-improvement

Read this file. Reflect on what this close-out found:

- Was there a category of cleanup that isn't covered by any step?
- Was any step too vague to execute precisely?
- Was any step unnecessary for this kind of work?

**Two targets — decide which each finding belongs to:**

- **About the flow** (applies in any repo) → a proposal for this skill's source repo (the `repository` in the plugin's `.claude-plugin/plugin.json`), in its `skills/close-out/IMPROVEMENTS.md`. **Don't edit this SKILL.md directly** — it's shared across every repo, and an installed plugin copy is overwritten on the next update anyway. Surface the proposal to the user first. The source repo usually isn't the current one: draft the entry, and write and commit it in a clone of that repo only if the user says so.
- **About this repo** (a gate to add, a doc to track) → propose a diff to `.claude/close-out.md` and apply it after the user approves.

**Dedupe before writing.** Repetition inside a proposals file is evidence a theme was missed, not noticed.

Search the file's `## ` headings for 2–3 keywords from your theme (Grep tool, case-insensitive).

- **0 matches** → write the proposal.
- **1–2 matches** → don't write a new entry; append your evidence (date, what happened, commit SHA) to the existing one.
- **3+ matches** → stop proposing. File a GitHub issue with the recurrence count and links to every prior entry, and add one line to the existing entry pointing at it.

---

## Step 7 — Land what close-out itself changed

Steps 2–6 usually edit things after Step 1's commit: doc fixes, config changes, and the run log. Land them now so the session doesn't end on a dirty tree.

1. Run the config's `## Run log` command, if there is one.
2. Commit exactly the paths steps 2–6 and the run log touched, using the Step 1 pathspec rule. Push per policy.
3. `git status` should show none of *your* paths. Other sessions' changes aren't yours; leave them.

For a parked session, first give the return date, the wake-up trigger and the `/compact` line, then use this closing banner instead of the standard one below:

```
---------------------------------
Session parked until <when>
---------------------------------
```

**Closing report.** Default: a short scannable summary — what was committed (with hashes), issues opened or closed, anything needing the user's call, and what was deliberately left uncommitted. Real hashes and issue numbers, so it doubles as a receipt. If the config's `## Closing message` gives a report format, use that instead. If a write was denied or failed, say what landed and what didn't; never report success you didn't confirm.

Then output exactly this as the final message (or the banner the config's `## Closing message` sets):

```
---------------------------------
Session is now closed out
---------------------------------
```
