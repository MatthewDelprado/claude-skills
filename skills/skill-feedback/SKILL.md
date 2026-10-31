---
name: skill-feedback
description: Log feedback about a skill in this repo as a GitHub issue, drafted for the user to confirm before anything is filed. Use when the user says to log, report or raise feedback on a skill ("log that", "that view was wrong", "raise an issue"), or accepts a feedback line offered by explain-code, show-me or mock-up.
---

Feedback repo: `MatthewDelprado/claude-skills`

Turn a moment where a skill got it wrong, or got it right in a way worth keeping, into a GitHub issue. The user stays in control of what is filed.

## Steps

1. **Gather.** Skill name, which view or choice it made, the user's prompt, the user's own words on what went wrong, what they expected if they said, the name of the repo they were working in, and which signal fired (`redirect`, `trim`, `no fit`, `guessed`, `bad hand-off`, or `user-reported`).
2. **Leave code out.** No code, file contents or file paths from the session. The issue may be read outside the work repo. If the prompt contained code, paraphrase it.
3. **Check for a duplicate.** `gh issue list -R MatthewDelprado/claude-skills -l <skill> --state open -S "<keywords>"`. If a close match exists, offer to add a comment to it instead of a new issue.
4. **Draft and show it.** Title is short and specific ("explain-code: call tree too deep for a two-step flow"). Body:

```
Skill: explain-code
Chosen: call tree
Prompt: <the user's prompt, paraphrased if it held code>
What went wrong: <the user's words>
Expected: <what they wanted, if they said>
Repo: <working repo name>
Signal: <redirect | trim | no fit | guessed | bad hand-off | user-reported>
```

5. **Wait for a yes.** Do not file without it. Edit the draft if the user wants changes.
6. **File it.** Create the label if needed, ignoring the error when it already exists, then file:

```bash
gh label create <skill> -R MatthewDelprado/claude-skills 2>/dev/null || true
gh label create feedback -R MatthewDelprado/claude-skills 2>/dev/null || true
gh issue create -R MatthewDelprado/claude-skills -l <skill>,feedback -t "<title>" -b "<body>"
```

7. Give the user the issue URL. One line.

If `gh` is missing or not signed in, show the draft for pasting and mention `gh auth login`.

## Related skills

- `explain-code`, `show-me` and `mock-up` offer a one-line feedback prompt when a signal fires.
- `skill-review` turns accumulated issues into a PR.
