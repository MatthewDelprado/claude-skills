# claude-skills

Personal Claude Code skills that work in any repo.

## Skills

| Skill | What it does |
|---|---|
| [`rename-session`](skills/rename-session/SKILL.md) | Retitles the current session to `<overall work> - <#issue> - <mode> - <specifics>`, with prefixes for *needs you*, *parked until <time>*, *closing out* and *done*. Trigger: `/rename-session`. |

## Install

Personal (all repos on this machine):

```bash
gh repo clone MatthewDelprado/claude-skills ~/.claude/claude-skills
ln -s ~/.claude/claude-skills/skills/rename-session ~/.claude/skills/rename-session
```

Single repo (checked in with the project):

```bash
mkdir -p .claude/skills && cp -R ~/.claude/claude-skills/skills/rename-session .claude/skills/
```

Update later with `git -C ~/.claude/claude-skills pull`.

## Requirements

`rename-session` renames through the Claude desktop app's session tools (`mcp__ccd_session_mgmt__set_session_title`). In a plain terminal without them it prints the title for you to apply with `/rename`.
