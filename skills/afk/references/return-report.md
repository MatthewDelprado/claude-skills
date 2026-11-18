# afk return: report and catch-up cards

## The report

Write for someone who has been gone for hours and remembers only roughly what they asked for. Lead with outcomes, not activity.

```
# afk report: <goal>

<When you left> → <when it finished>. <One or two sentences: where things stand now.>

## Needs you (<N>)
1. <decision or queued action, one line each, in the order the walk will take them>

## What got done
<Per workstream: outcome · where it lives (branch / path / commit) · verified? (how) or not verified (why)>

## Versions built
<Per fork: the question · each variant, where it lives, how it differs in one line · my pick and why>

## Assumptions I made
| # | Choice | Picked | Not picked | To flip |
|---|---|---|---|---|

## Queued for your approval
<Each one: what it does, and the exact command, draft or diff in full>

## Not done
<What's left, and why: blocked on what, or out of scope>

## Dead ends
<What was tried and dropped, one line each, so nobody repeats it>
```

Drop any section that would be empty. Link every branch, file and page.

## The catch-up card (one per turn)

Each card stands alone. The user may have forgotten the goal, the run, and every card before this one.

```
**Decision <n> of <N>: <short title>**

**Background:** <what you originally asked for that led here, in one or two sentences>
**When you left:** <how things stood on this point>
**While you were away:** <what I did about it: built, tried, ruled out>
**The question:** <one line>

a) <option> — <what it means in practice> · <link to variant if built>  ← recommended
b) <option> — <…>
c) <option> — <…>

**Why I'd pick a:** <one or two lines>
**What happens next:** <what I'll do on each answer, e.g. "a: merge branch afk/x-a, delete -b and -c">
```

Keep it under about 15 lines. For a queued outward action, put the full artefact (the draft, the diff, the exact command) on the card. A one-word answer counts as approval only for what's shown.

After their answer: act on it, say in one line what you did, then show the next card. Show `(<k> left)` only when the count changes or every few cards.
