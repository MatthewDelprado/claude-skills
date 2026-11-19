# close-out setup — the interview and the config template

Read only when there is no `.claude/close-out.md` or `MODE=setup`. For `setup` with an existing config, start from it and amend; don't redo what's settled.

One question per turn, each with a recommended default, answerable in a word. Not a form.

**1. Survey silently.** Read-only; never ask what a lookup answers.

- `CLAUDE.md`, `AGENTS.md`, `README`, `CONTRIBUTING`: stated conventions for commits, PRs, docs, memory
- Docs describing the system (`CONTEXT.md`, `ARCHITECTURE.md`, `docs/`, ADRs, `CHANGELOG`) and where handoff notes already live (`sessions/`, `notes/`)
- Checks: `.github/workflows`, and test/lint/typecheck/build scripts in `package.json` / `Makefile` / `justfile`
- Git: default branch, remote, merged PRs vs direct pushes, worktrees or other signs of concurrent sessions
- Issues: `gh repo view`, `gh label list`, a few recent issues (labeling convention, any in-progress label)
- Duplicated or generated files that drift (mirrors, copies of one doc); noise patterns in `.gitignore`

**2. Draft candidates.** For each item the evidence supports, note what you found and a recommended default. Nothing found, no candidate. **Don't invent steps to fill a section**; a bare repo gets a minimal config (summary, commit, push) and you say so.

**3. Ask.** Open with the shortcut: "Found N candidate steps — walk through them, or start minimal?" Then in this order, skipping anything with no evidence (except the two policy choices, which are always asked):

1. Session record: summary file (default), a line in an existing log, both, or none. If the survey found a log the repo already keeps, recommend that *(policy)*
2. Push policy: direct to the default branch, PR, or don't push *(policy)*
3. Changes this session didn't make: only if the survey shows hand-edited content or high-blast-radius files (schema, CI, agent instructions); name them as path classes
4. Docs that must stay current
5. Duplicated or generated files to reconcile
6. Gates: commands to run, and whether failure stops, asks, or warns
7. Issue tracker: repo, labeling convention, claim label
8. "Anything you always do at the end of a session here that I haven't listed?"

Record only what differs from the defaults in SKILL.md; a config that restates a default is noise that drifts.

**4. Write `.claude/close-out.md`** from the template, show it in full, and continue into the run. It's committed with the session's work.

## Config template

Omit any section with nothing in it.

```markdown
# close-out config — <repo>

## Session summary
- Path: `<dir>/YYYY-MM-DD-<slug>.md`        (or: none)
- Log: `<file>`, one line per change, format `<line format>`   (optional; with Path: none, the log is the only record)
- Anything the default template must keep or add

## Git
- Branch and push policy
- Hand-edited paths: `<globs>` — policy: commit separately | leave | ask   (opt-in; without this line, pre-existing changes are left and named in the report)
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

## Parked sessions
- Wake-up mechanism (reminder command or tool)

## Self-improvement
- Where repo-level proposals go

## Run log
- command, if the repo keeps one

## Skip
- Steps to omit, with the reason

## Closing message
- Report format: default | <template>
- Banner: default | <custom text>
- (Legacy: bare free-form text under this heading, from before these keys, is treated as the banner.)
```
