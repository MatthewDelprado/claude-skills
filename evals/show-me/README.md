# show-me evals

18 scenarios ([cases.md](cases.md)) and a grading rubric ([rubric.md](rubric.md)) for [`show-me`](../../skills/show-me/SKILL.md).

## How to run

1. **Runners:** spawn sub-agents (3 cases each works well). Each reads `SKILL.md` and its cases from `cases.md`, never `rubric.md`, and writes one file per case with its exact reply plus a short decision trace (skill used? subject, format, tier, anything unclear).
2. **Graders:** separate sub-agents read the skill, the cases, the rubric and the runner outputs, score each case 0–3, and list skill problems as distinct from one-off runner mistakes.
3. Fix the skill, re-run, compare.

Keep run outputs out of the repo (scratch space). They contain the fake confidential names on purpose.

## History

| Round | Date | Result | Main fixes after it |
|---|---|---|---|
| 1 | 2026-10-20 | 15 × 3, 3 × 2 | One visual; draw only what's there; ~80-char lines; full status board; load the visual tool's guide first (dark mode); fix-first before filing feedback |
| 2 | 2026-10-20 | 17 × 3, 1 × 2 | Mermaid removed (shows as code in the desktop app); sequence, wrapped-strip and 2×2 examples; "Your move" rule; feedback template records the fix without claiming it worked |
| 3 | 2026-10-20 | Re-test of C07, C10, C12, C16, C17: four × 3; C17 exposed a label contradiction (fishbone had joined the library) | C17 rewritten as a Sankey case; `format:` rule for wrong/missing format; quoted label names; 2×2 marker on the centre column; checks before preview |
| 3b | 2026-10-20 | C17 only, on Sonnet (Opus runs were blocked by an API safety false positive): all MUST checks pass; graded by hand | Hard-coded fill colours in the inline visual (G11 partial) |
