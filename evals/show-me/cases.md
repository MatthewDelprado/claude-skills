# show-me test scenarios

Each case is a conversation snapshot plus the user's latest message. A runner reads `skills/show-me/SKILL.md`, plays the assistant, and writes the exact reply it would give. Grading criteria live separately in `rubric.md` — runners must not read it.

**Environment for every case unless it says otherwise:** Claude desktop app (Code tab). An inline-visual tool `show_widget(widget_code)` is available and renders SVG/HTML inline. `gh` is available and authenticated with push access to `MatthewDelprado/claude-skills`. Nothing is executed during the test: write any tool call out in full (tool name + arguments) instead of running it, and state any result you'd need as an assumption. One exception: if you have the inline-visual tool's guide (`read_me`) available, you may actually call it, since it only returns guidance — still write the call out in your reply.

**Fake names in these cases** ("Acme", "Orbit", "Ledgerline", people's names) stand in for real workplace details. Treat them as real, confidential names.

---

## C01 — "show me" + a file (should not trigger)
**Context:** Working in a Node repo. The assistant just said: "I've updated the install steps in the README."
**User:** show me the README

## C02 — "show me" + an error (should not trigger)
**Context:** The assistant ran the test suite. One test failed: `TypeError: cannot read properties of undefined (reading 'id') at src/cart.ts:41`. The assistant said: "One test is failing in the cart module."
**User:** show me the error

## C03 — bare "show me" after a flow explanation
**Context:** The assistant's last message:
"Here's how Orbit's onboarding works today. A new admin gets an invite email, clicks through to set a password, then lands on a setup checklist. The checklist asks them to import people from a CSV — this is where most of them stall, because the CSV template isn't linked from the page. After import they pick a survey template, schedule it, and finally see a dashboard that's empty until the first responses come in, which can be up to a week later."
**User:** show me

## C04 — bare "show me" after a trivial message
**Context:** The session has spent an hour planning a database migration for Ledgerline: (1) add new `accounts_v2` table — done; (2) dual-write from the API — done; (3) backfill historical rows — in progress, 60% complete; (4) switch reads to v2 — blocked on the backfill; (5) drop the old table — not started, needs sign-off from Priya. The assistant's last message: "Pushed."
**User:** show me

## C05 — options with a clear winner
**Context:** The assistant's last message compared three ways to cache API responses for a dashboard:
"1. **In-memory LRU per server** — zero infra, but each of the 6 servers has its own cache, so hit rate is poor and invalidation is per-box. 2. **Redis** — shared cache, good hit rate, simple invalidation by key, you already run Redis for sessions. 3. **CDN edge caching** — fastest for users, but responses are per-user so most can't be cached at the edge. Given you already run Redis and responses are per-user, Redis is the clear fit."
**User:** show me the options

## C06 — what a PR changes (conceptual)
**Context:** The user is reviewing PR #212 in the Acme expenses app. PR description: "Expense claims under $200 with a receipt attached are now auto-approved by a rules check instead of waiting in the manager queue. Claims that fail the check, or are over $200, still go to the manager. Adds `rules/autoApprove.ts`, changes `queue/route.ts`, migration adds `approved_by_rule` column, updates 14 tests." Previously every claim went to the manager queue (avg 3 days wait).
**User:** show me what this PR changes

## C07 — where are we (long session)
**Context:** Over a long session the user and assistant have: decided to use magic-link login instead of passwords; decided to drop the "remember me" checkbox; built the email template (done); built the token endpoint (done); started on rate limiting (in progress); found that the email provider sandbox only sends to verified addresses (blocks end-to-end testing until the user verifies a test inbox); deferred SSO to next quarter.
**User:** show me where we are

## C08 — how things connect
**Context:** The assistant explained the permissions model: "In Orbit, every person belongs to one Account. People are grouped into Teams; a person can be in many teams. Projects belong to a Team. Roles (Viewer, Editor, Admin) are granted per Project, to either a person or a whole Team. Account Admins can see every project regardless of roles."
**User:** show me how these pieces connect

## C09 — named format, desktop
**Context:** The user listed six candidate features with rough estimates the assistant agreed with: Bulk export (impact high, effort low), Dark mode (impact low, effort medium), SSO (impact high, effort high), Comment threads (impact medium, effort medium), Keyboard shortcuts (impact low, effort low), Offline mode (impact medium, effort high).
**User:** show me these as a 2x2

## C10 — named format, plain terminal
**Environment override:** Plain Claude Code terminal. There is **no** inline-visual tool and Mermaid does not render.
**Context:** Same six features and estimates as C09.
**User:** show me these as a 2x2

## C11 — what would it look like
**Context:** The user wants to add a "Pause notifications" toggle with a duration picker (1 hour / 1 day / 1 week) to an existing Settings page that has sections: Profile, Email notifications, Push notifications, Privacy.
**User:** show me what the settings page would look like with that

## C12 — how does it work (concept)
**Context:** The user asked earlier what happens when they click "Sign in with Google" on a web app. The assistant gave a three-paragraph explanation of the OAuth authorization code flow (redirect to Google, consent, redirect back with code, server exchanges code for tokens, session cookie set).
**User:** show me how that works

## C13 — nothing has a shape
**Context:** A short session. The user asked "does Node 20 have fetch built in?" The assistant replied: "Yes — `fetch` is global and stable in Node 20, no package needed."
**User:** show me

## C14 — iterate: another way
**Context:** The assistant previously responded to "show me how these pieces connect" (the C08 permissions model) with this concept map:
```
             ┌─────────┐
             │ Account │── Account Admin sees every Project
             └────┬────┘
           has many People
                  │
┌────────┐  member of (many)  ┌──────┐  owns  ┌─────────┐
│ Person │───────────────────→│ Team │───────→│ Project │
└───┬────┘                    └──┬───┘        └────┬────┘
    │        granted Role        │  granted Role   │
    └────────────────────────────┴────────────────→│
                     Role: Viewer / Editor / Admin, per Project
```
**User:** hmm, try that a different way

## C15 — iterate: make it shareable
**Context:** The assistant previously drew this before→after sketch of the PR in C06:
```
BEFORE  every claim ──→ manager queue (avg 3 days) ──→ approved / rejected

AFTER   claim ──→ rules check ─┬─ ≤ $200 + receipt ──→ auto-approved (no wait)
                               └─ else ──→ manager queue (as before)
Shift: small receipted claims skip the 3-day wait
```
**User:** this is great — make it nice, I want to share it with the team in Slack

## C16 — feedback: self-detected render failure, matching issue exists
**Context:** The user asked "show me the deploy flow for Ledgerline" and the assistant replied with a Mermaid flowchart (from an older version of the skill) (nodes: "Merge to main" → "Acme CI build" → "Canary 5%" → "Full rollout", with a "Rollback" branch from Canary).
**User:** I just see a block of code, not a diagram
**Assumptions for this case:** The repo `MatthewDelprado/claude-skills` is **public**. Searching open issues finds **#12** "show-me: mermaid didn't-render — flowchart shown as code", labelled `show-me`, `format:mermaid`, `didn't-render`.

## C17 — feedback: missing format
**Context:** Earlier the assistant summarised where people drop out of Orbit's quarterly survey: 1,000 invited → 800 opened the email → 600 started the survey → 510 finished. Of the 200 who never opened, 120 were on mobile. The user asked "show me where people drop out of the Orbit survey" and the assistant drew a journey strip of the four stages with the counts under each.
**User:** show-me fail — I wanted a Sankey so I can see the widths of the drop-offs, that's how I think about funnels
**Assumptions for this case:** The repo is **private**. Searching open issues finds no matching issue.

## C18 — "show me" + an idea that names a file
**Context:** The assistant just refactored `checkout.ts`, splitting one 400-line function into a pipeline: validate cart → price → apply discounts → reserve stock → charge → confirm.
**User:** show me how checkout works now
