---
name: rename-session
description: Rename the current Claude Code session so its sidebar title says what the session is doing right now — "<overall work> - <#issue> - <mode> - <specifics>", plus a state prefix when blocked on the user ("Needs you: <what> - "), parked until a set time ("<wake time> - "), closing out ("Closing out - ") or finished ("Done - "). Trigger on "/rename-session", "rename this session", "retitle this", "fix the session name". Other skills can call it at state changes with an explicit STATE.
---

# rename-session

Make the session's sidebar title say what the session is doing *now*. When several sessions run in parallel, the title is how you pick the right one, and auto-generated titles only describe the opening message.

Works in any repo. Needs the Claude desktop app's session tools (`mcp__ccd_session_mgmt__*`). Without them, build the title anyway and print it for the user to apply with `/rename`.

---

## Title format

```
<overall work> - <#issue> - <mode> - <specifics>
```

Example: `Payments API - #396 - grill - retry policy`

- **Overall work:** the umbrella effort (e.g. "Payments API", "Onboarding redesign", "Flaky CI"). Reuse the existing segment if it still fits; a stable name makes the sidebar easy to scan.
- **#issue:** the GitHub issue currently being worked (claimed, commented on, or named by the user). Omit the segment if there's none. If the work moved to a different issue, use the new one.
- **Mode:** what kind of work is happening right now: `grill`, `build`, `debug`, `review`, `triage`, `research`, `verify`, `close-out`, etc.
- **Specifics:** 2–4 words on the concrete topic.

Base the title on what the session is doing *now*, not what it opened with.

## State prefixes

Only ever one prefix. Precedence if more than one applies: `closing` > `waiting` > `parked`.

| STATE | Meaning | Prefix |
|---|---|---|
| `auto` (default) | Work out the state from the conversation | whichever fits below |
| `working` | Actively working | none (strip any state prefix) |
| `waiting` | Blocked until the user does something (setup step, decision, approval, physical check) | `Needs you: <NEED> - ` |
| `parked` | Kept open and idle until a set time | `<WHEN> - ` |
| `closing` | Wrap-up/close-out has started | `Closing out - ` |
| `done` | Wrap-up finished and nothing is left to come back for | `Done - ` |

- `NEED` is 2–4 words naming what the user has to do ("1Password setup", "approve PR", "pick option", "check garage door"). Name the action, not the reason. Required for `waiting`.
- `WHEN` is the wake time as the user would say it ("Monday 9am", "Sun 4 Oct 10am", "Tomorrow 7pm"). Required for `parked`.

**In `auto`:**
1. If the last turn ended by handing the user a to-do or a question the work can't proceed without → `waiting`, with `NEED` taken from it.
2. Else if a reminder or watcher was just set, or the work is done for now and the next step is a check at a known time (a soak, a deploy verification, a reply due by then) → `parked`, with that time as `WHEN`. Set the mode to what happens on return (usually `verify`), not the work that just finished.
3. Else → `working`.

`auto` never picks `done` or `closing`; only a wrap-up flow sets those.

## Calling it from other skills

Other skills (a close-out, a planning/grilling skill, a "what's next" walkthrough) can call this at state changes without asking the user anything: just rename and carry on.

| When | Call |
|---|---|
| Wrap-up starts (first act) | `rename-session STATE=closing` |
| Wrap-up ends, something due later | `rename-session STATE=parked WHEN=<time>` |
| Wrap-up ends, user has a follow-up | `rename-session STATE=waiting NEED=<what>` |
| Wrap-up ends, nothing left | `rename-session STATE=done` |
| Planning ends and building starts | `rename-session` |
| Handing the user a blocking to-do and stopping | `rename-session STATE=waiting NEED=<what>` |

## Steps

1. **Check for a repo override:** if `.claude/session-title.md` exists in the repo, read it. It can change the format, mode vocabulary or prefixes, and wins over the defaults above.
2. **Get the current title:** `mcp__ccd_session_mgmt__get_session` with `session_id: "self"`. Load it with ToolSearch (`select:mcp__ccd_session_mgmt__get_session,mcp__ccd_session_mgmt__set_session_title`) if it's deferred.
3. **Build the base title** from what the session is doing now. Strip any existing state prefix (`Closing out - `, `Needs you: … - `, `<time> - `, `Done - `) before comparing.
4. **Apply the state prefix** from the table.
5. **Skip if nothing changed.** If the new title equals the current one, don't call the rename tool.
6. **Rename:** `mcp__ccd_session_mgmt__set_session_title` with `session_id: "self"`. If the user set the current title themselves, the app asks them to approve; if they decline, leave it and don't retry.
7. **Report in one line** (`Renamed: <new title>`), or say nothing if a caller skill is mid-flow and the rename is incidental. Never more than one line.

## Repo override example

`.claude/session-title.md`:

```markdown
Format: <project> - <mode> - <specifics>   (we don't use issue numbers here)
Modes: spec, build, review, ship
Overall work names: "Checkout", "Search", "Infra"
```
