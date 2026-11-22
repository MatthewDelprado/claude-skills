# close-out config — claude-skills

## Session summary
- Path: none. The PR description and issue comments are the record; this public repo keeps no session notes.

## Git
- Every change lands through a PR, squash-merged. Never push to `main`. Commit close-out's own changes on a branch, push it and open a PR.

## Docs
| File | Check |
|---|---|
| `README.md` | When a session adds a skill or changes what one does: every folder in `skills/` has a row in the skills table, and each row still describes what that skill does. |

## Gates
### check.py
- **When:** always, before pushing
- **On fail:** stop
- `python3 scripts/check.py` (CI runs the same check)

### No workplace specifics
- **When:** always, before committing
- **On fail:** stop
- `git config user.email` is the personal address, not a work one.
- The diff, commit messages and any PR title or body name no employer, client, internal product or team, work email, work GitHub handle, internal URL or internal tool (see `CLAUDE.md`).

## Issues
- Repo: `MatthewDelprado/claude-skills`. No in-progress label, so claims are a comment only.
- Every issue filed gets two labels: the skill's name (for example `close-out`, `show-me`; create it if missing) and a type: `feedback`, `enhancement` or `bug`.

## Extra steps
### After Step 7 — Update the local plugin
If a PR merged to `main` this session, run `claude plugin marketplace update dp-skills`, then `claude plugin update dp@dp-skills`, and say a restart is needed to load it.
