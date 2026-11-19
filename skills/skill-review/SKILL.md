---
name: skill-review
description: Review open feedback issues for a skill in this repo and open a PR with proposed edits for the user to review and merge. Run on demand with /skill-review <skill> or /skill-review all. Runs start to finish without asking questions.
disable-model-invocation: true
---

Repo: `MatthewDelprado/claude-skills`

Read the open feedback for a skill, find the patterns, and propose edits as a pull request. The user reviews and merges. Never merge.

This command must run unattended. It asks no questions mid-run, so it can be scheduled later. Where something is unclear, skip that change and say so in the PR body.

## Steps

1. **Get a clone.** If the working directory is not a clone of the repo, run `gh repo clone MatthewDelprado/claude-skills "${TMPDIR:-/tmp}/claude-skills"` and work there. Start from an up-to-date `main`.
2. **Read the issues.** `gh issue list -R MatthewDelprado/claude-skills -l <skill> --state open --json number,title,body,comments --limit 100`. For `all`, repeat per skill under `skills/`.
3. **Group by pattern.** Same cause, same direction of fix.
4. **Apply the two-issue rule.** Change a skill only for a pattern backed by two or more issues. Single issues stay open and are listed in the report.
5. **Tighten as you go.** The net line count of the skill's `SKILL.md` must not grow. If a fix needs room, merge duplicate guidance or drop the instruction with the least evidence behind it. A skill stays at 100 lines or fewer. Move bulky detail into `references/`.
6. **Check.** Run `python3 scripts/check.py`. It must pass before anything is pushed.
7. **Open the PR.** Branch `skill-review/<skill>-<yyyy-mm-dd>`, commit, push, then `gh pr create`. The body lists each pattern, the change made, and `Closes #n` for every issue it resolves. Add a short section for issues skipped and why.
8. **Report.** Give the PR URL, or if no pattern reached two issues, the counts per pattern and no PR.

## Related skills

- Issues come from `skill-feedback`, usually offered by `explain-code`, `show-me` or `mock-up`.
