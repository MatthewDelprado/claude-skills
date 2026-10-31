# claude-skills

Personal Claude Code skills that work in any repo. No repo-specific paths or tools baked in. Each skill has universal defaults, and a repo can override any of them with a config file (`.claude/close-out.md`, `.claude/session-title.md`) that records only what differs there.

## Skills

| Skill | What it does |
|---|---|
| [`rename-session`](skills/rename-session/SKILL.md) | Retitles the current session to `<overall work> - <#issue> - <mode> - <specifics>`, with prefixes for *needs you*, *parked until <date>*, *closing out* and *done*. Trigger: `/rename-session`. |
| [`close-out`](skills/close-out/SKILL.md) | End-of-session cleanup: session summary, commit only this session's work, stale-reference audit, docs and verification check, issue tidy-up, self-improvement proposals. Repo-specific steps come from `.claude/close-out.md`; the first run in a repo interviews you to create it. Trigger: "close out", "wrap up". |
| [`whats-next`](skills/whats-next/SKILL.md) | Walks you through the remaining work one decision per turn, each with a recommended default, until the session is blocked or done, then hands off to `close-out`. Trigger: "what's next", "what's left". |
| [`bro`](skills/bro/SKILL.md) | Makes the last message easier to understand: restates it in plain language with no jargon, tables any options with factors and a recommendation, and opens with a very brief summary (one or two sentences) when the conversation is deep in detail. Trigger: "bro", "wtf". |
| [`show-me`](skills/show-me/SKILL.md) | Explains something visually in chat: picks the right diagram form, renders Mermaid through `show_widget` (the Mermaid connector's output is too large to display), and offers to install the right connector when the render tool is missing. Trigger: "show me visually", "draw this as a diagram", "diagram this flow", "diagram this system", "visualize this as a diagram". |
| [`explain-code`](skills/explain-code/SKILL.md) | Explains code, a code flow, a refactor or a change in chat with the smallest useful view: pseudocode, call tree, component tree, file tree, small Mermaid diagram, or diff. Trigger: "sketch the flow", "draw the call tree", "what would change". |
| [`mock-up`](skills/mock-up/SKILL.md) | Builds a throwaway HTML preview of a UI idea in the current repo's own look and feel. Trigger: "mock this up", "what would this look like". |
| [`grill-me`](skills/grill-me/SKILL.md) | Interviews you about a plan one question at a time, with a live decision-tree page that keeps IDs stable. Trigger: "grill me". |
| [`skill-feedback`](skills/skill-feedback/SKILL.md) | Logs feedback on a skill as a GitHub issue on this repo. It drafts the issue and you confirm before anything is filed. |
| [`skill-review`](skills/skill-review/SKILL.md) | Reads the open feedback issues for a skill and opens a PR with proposed edits. You review and merge. Trigger: `/skill-review <skill>`. |

`close-out`, `whats-next` and `rename-session` cooperate if all are installed: `close-out` and `whats-next` call `rename-session` at state changes, and `whats-next` hands off to `close-out`. Each works alone, and `bro` and `show-me` stand alone. `explain-code` and `mock-up` name each other and `show-me`, and offer a one-line `skill-feedback` prompt when a skill gets it wrong; `skill-review` turns the accumulated issues into a PR.

## Install

As a plugin (recommended; works on any machine, updates itself):

```
/plugin marketplace add MatthewDelprado/claude-skills
/plugin install dp@dp-skills
```

Skills then appear namespaced, e.g. `dp:close-out`, `dp:whats-next`, `dp:rename-session`, `dp:bro`, `dp:show-me`, `dp:explain-code`, `dp:mock-up`, `dp:grill-me`, `dp:skill-feedback`, `dp:skill-review`. Updates arrive when the Claude app launches, if auto-update is on for the marketplace (`/plugin` > Marketplaces > dp-skills). In the desktop app, starting a new session isn't enough: quit and reopen the app, or pull straight away with `claude plugin marketplace update dp-skills`.

The plugin has no `version` on purpose, so every push to `main` counts as an update.

Editing: work in a normal clone of this repo, push, and the change reaches each machine the next time its Claude app is restarted.

Installed on: a personal Mac and a work Mac. The work Mac pushes through a second GitHub account added as a collaborator with write access.

If a machine's admin settings block third-party marketplaces, fall back to symlinks:

```bash
gh repo clone MatthewDelprado/claude-skills ~/.claude/claude-skills
for s in rename-session close-out whats-next bro show-me explain-code mock-up grill-me skill-feedback skill-review; do ln -s ~/.claude/claude-skills/skills/$s ~/.claude/skills/$s; done
```

## Requirements

- `rename-session` renames through the Claude desktop app's session tools (`mcp__ccd_session_mgmt__set_session_title`). In a plain terminal without them it prints the title for you to apply with `/rename`.
- `show-me` renders through the Claude desktop app's `show_widget` tool (`mcp__visualize__*`). Without it, it offers a connector via the MCP registry, then falls back to a fenced `mermaid` block.
- `close-out` uses `git` and, for the issue steps, the `gh` CLI. Outside a git repo it skips the git steps.

## Feedback loop

When `explain-code` or `mock-up` gets it wrong (you asked for a different view, trimmed the output, or it had to guess), it ends with one line offering to log it, at most once per session. Say yes and `skill-feedback` drafts a GitHub issue on this repo for you to confirm. Run `/skill-review <skill>` now and then: it groups the open issues, changes a skill only where two or more agree, and opens a PR that must not grow the skill. You review and merge.

## Adding things

1. Create `skills/<name>/SKILL.md` with `name` (matching the folder) and `description` frontmatter.
2. Add a line under Related skills in at least one sibling that names it. A skill that stands alone goes in `STANDALONE` in `scripts/check.py`.
3. Add it to the README table, the `dp` descriptions in `.claude-plugin/`, and the symlink loop above.
4. Run `python3 scripts/check.py`. CI runs the same check on every PR.

Keep each `SKILL.md` at 100 lines or fewer and put detail in `references/`. `close-out` and `whats-next` predate the cap and are listed in `LONG_SKILLS`.

## Layout

```
.claude-plugin/marketplace.json
.claude-plugin/plugin.json
skills/<name>/SKILL.md
skills/<name>/references/
scripts/check.py        # layout, frontmatter, size cap, sibling links
.github/workflows/      # check.yml (layout check), claude-review.yml (PR review)
```

## Credits

`explain-code` started from humanlayer's `show-me` skill (MIT), trimmed and extended. It was renamed when this repo absorbed the former `Dp-Skills` repo, because this repo already had a different `show-me`.
