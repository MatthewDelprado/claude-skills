# claude-skills — repo rules

## No workplace specifics

This repo is public and installed on both personal and work machines. Never name a workplace in it: no employer or client names, internal product or team names, work email addresses, work GitHub account handles, internal URLs, or internal tool names.

This covers everything that lands in the repo or its history: skill files, the README, manifests, commit messages, PR titles and descriptions, and commit author emails. Say "a work machine" or "the work repo" instead.

Workplace-specific behaviour belongs in that workplace's own repo, as a config override (`.claude/close-out.md`, `.claude/session-title.md`), never here.

## Known history

A few early commits predate this rule and carry a work author identity. They were left in place on purpose: rewriting `main` would break every clone and the installed plugin. Reviewers should not flag the commits already on `main` as of this note; any new commit with a work identity must still be flagged. New commits must not repeat it: on a work machine, check `git config user.email` before committing here.
