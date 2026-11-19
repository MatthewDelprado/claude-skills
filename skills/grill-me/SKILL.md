---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Keep a live page

Each question lives on a single page the user can glance at: the decision tree on top, the current question below it. Update the same page every turn. The chat reply stays short.

Start from `references/page-template.html`. Everything the page shows comes from the `GRILL` data block between `/*DATA*/` and `/*END*/`. Edit only that block. The tree and the question heading are both rendered from `decisions`, so they cannot disagree.

### Numbering

- Every decision gets an ID when it is created: `D1`, `D2`, `D3`. The next unused number, always.
- IDs are identity, not position. Never renumber, reuse or skip back. Tree order follows dependency, so a new `D9` can sit under `D2`. Use `parent` to place it.
- The question heading is the ID of the decision being asked (`D7 · Title`). `GRILL.current` and `GRILL.question.id` must both equal that ID.
- When an answer changes an earlier decision, keep its ID, update `answer`, and set `status` to `revised`. Do not add a new row for the same decision.
- When an answer opens new decisions, add them as new IDs with `parent` set, status `pending`. When one question settles two decisions, settle both rows and say so in chat.
- Status values: `settled`, `revised`, `open`, `pending`.

### Each turn

1. Update the data block: mark the answered decision `settled` (with a one-line `answer`), add any new decisions, pick the next open decision as `current`, and write its `question` (`prompt`, plus `html` for the options).
2. Republish or reopen the page (see below).
3. Reply in chat with the question, your recommended answer and why, in a few lines, plus the link. Do not repeat the tree in chat.

For `question.html`, use the template's classes: `.opts` with `.opt` cards, `.opt.rec` plus `<span class="tag">RECOMMENDED</span>` on the one you recommend, `pre` for a small diagram or example, `.why` for the trade-off, and `table` for comparisons. Show the shape of the choice, not a wall of text. Skip the options grid when a recommendation and one diagram say it better.

### Publishing

- With an Artifact tool: write the file under the outputs folder, publish it, and on every later turn republish with the same `url` so it is one living page, not a new one per question.
- In a terminal agent: write `$TMPDIR/grill-me/grill-{topic}.html`, overwrite it each turn, and open it once with `open`, `xdg-open` or `start` for the OS. Later turns only need a browser refresh.
- If neither works, fall back to the plain chat interview and say so once.

### Finishing

When no decision is `open` or `pending`, set `current` to `null`. The page then renders an agreed-design table of every ID, title and answer, plus `followups`. Say in chat that the tree is closed, and list the follow-ups.
