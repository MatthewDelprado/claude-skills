# claude-skills

Personal Claude Code skills that work in any repo. No repo-specific paths or tools baked in. Each skill has universal defaults, and a repo can override any of them with a config file (`.claude/close-out.md`, `.claude/session-title.md`) that records only what differs there.

## Skills

| Skill | What it does |
|---|---|
| [`rename-session`](skills/rename-session/SKILL.md) | Retitles the current session to `<overall work> - <#issue> - <mode> - <specifics>`, with prefixes for *needs you*, *parked until <time>*, *closing out* and *done*. Trigger: `/rename-session`. |
| [`close-out`](skills/close-out/SKILL.md) | End-of-session cleanup: session summary, commit only this session's work, stale-reference audit, docs and verification check, issue tidy-up, self-improvement proposals. Repo-specific steps come from `.claude/close-out.md`; the first run in a repo interviews you to create it. Trigger: "close out", "wrap up". |
| [`whats-next`](skills/whats-next/SKILL.md) | Walks you through the remaining work one decision per turn, each with a recommended default, until the session is blocked or done, then hands off to `close-out`. Trigger: "what's next", "what's left". |
| [`bro`](skills/bro/SKILL.md) | Makes the last message easier to understand: restates it in plain language with no jargon, tables any options with factors and a recommendation, and opens with a very brief summary (one or two sentences) when the conversation is deep in detail. Trigger: "bro", "wtf". |
| [`show-me`](skills/show-me/SKILL.md) | Explains something visually in chat: picks the right diagram form, renders Mermaid through `show_widget` (the Mermaid connector's output is too large to display), and offers to install the right connector when the render tool is missing. Trigger: "show me visually", "draw this", "diagram this", "visualize this as a diagram". |

`close-out`, `whats-next` and `rename-session` cooperate if all are installed: `close-out` and `whats-next` call `rename-session` at state changes, and `whats-next` hands off to `close-out`. Each works alone, and `bro` and `show-me` stand alone.

## Install

As a plugin (recommended; works on any machine, updates itself):

```
/plugin marketplace add MatthewDelprado/claude-skills
/plugin install dp@dp-skills
```

Skills then appear namespaced, e.g. `dp:close-out`, `dp:whats-next`, `dp:rename-session`, `dp:bro`, `dp:show-me`. Updates arrive when the Claude app launches, if auto-update is on for the marketplace (`/plugin` > Marketplaces > dp-skills). In the desktop app, starting a new session isn't enough: quit and reopen the app, or pull straight away with `claude plugin marketplace update dp-skills`.

The plugin has no `version` on purpose, so every push to `main` counts as an update.

Editing: work in a normal clone of this repo, push, and the change reaches each machine the next time its Claude app is restarted.

Installed on: a personal Mac and a work Mac. The work Mac pushes through a second GitHub account added as a collaborator with write access.

If a machine's admin settings block third-party marketplaces, fall back to symlinks:

```bash
gh repo clone MatthewDelprado/claude-skills ~/.claude/claude-skills
for s in rename-session close-out whats-next bro show-me; do ln -s ~/.claude/claude-skills/skills/$s ~/.claude/skills/$s; done
```

## Requirements

- `rename-session` renames through the Claude desktop app's session tools (`mcp__ccd_session_mgmt__set_session_title`). In a plain terminal without them it prints the title for you to apply with `/rename`.
- `show-me` renders through the Claude desktop app's `show_widget` tool (`mcp__visualize__*`). Without it, it offers a connector via the MCP registry, then falls back to a fenced `mermaid` block.
- `close-out` uses `git` and, for the issue steps, the `gh` CLI. Outside a git repo it skips the git steps.
