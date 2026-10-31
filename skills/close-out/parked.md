# Parked sessions — close out now, come back on a date

Read only when the session is parked: the user says so ("I'll check back on <date>", "don't archive") or the follow-up is a check at a known time (a soak, a week of traffic, a reply). The session stays open, not archived. A parked close-out runs every step as normal, plus:

1. **Return date.** Pin it as weekday, date and time ("Sat 17 Oct 10am"), never a relative word. That string is for the reminder and the return brief; the session title takes only `MM.DD`, so pass just that as `WHEN` to `rename-session` (`WHEN=10.17`).
2. **Return brief in the summary.** Step 0's `## Follow-up` opens with a `**Return <when>:**` checklist of exactly what to check on return and where to look (files, logs, commands), enough for someone who has forgotten the session.
3. **Wake-up trigger.** Something must ping the user at the return time: the repo's reminder mechanism (config `## Parked sessions`), a scheduling tool if available, or say plainly that none exists. Put the session's `link` (from `mcp__ccd_session_mgmt__get_session`, `session_id: "self"`, when the desktop app tools are available) and the return checklist in the reminder text.
4. **Issues.** Claimed issues still lose their in-progress label (Step 5). The hand-off comment names the return date and what will be decided then.
5. **Compaction.** A parked session re-sends its whole transcript each turn after the return. Claude can't compact itself, so end the closing message with a ready-to-paste line, e.g. `/compact Keep only: return brief from sessions/<file>.md, open decisions, and what to check on <when>. Drop the investigation detail.` Omit for short sessions.
6. **Closing message.** Give the return date, wake-up trigger and `/compact` line first, then end with this banner **instead of** the standard one (it wins over a custom `Banner:`):

```
---------------------------------
Session parked until <when>
---------------------------------
```
