# close-out — improvement proposals

Proposals from Step 6 runs. Each `## ` heading is one theme; add new evidence to an existing theme rather than opening a duplicate (see Step 6's dedupe rule).

## Work done in another repo or a scratch clone isn't checked

**Seen:** 2026-10-19. The session's real work was in a different repo from the one close-out ran in, edited through a temporary clone in the session's scratchpad. Step 1 only inspects the current repo, so it reported a clean tree with nothing to land, and none of the steps looked at the other repo. The scratch clone was also wiped when the session restarted partway through, so a commit left there unpushed would have been lost without any warning.

**Proposal:** add to Step 1:

- List every repo this session wrote to (from the conversation: `git -C <path>` commands, clones, `gh` PRs against another `--repo`), not only the current one.
- For each one, check for uncommitted changes, unpushed commits (`git -C <path> status -sb`), and branches or PRs the session opened that are still open. Report each, and treat work held only in a scratch or temp directory as at risk.
- Check the author email on this session's commits in each repo (`git -C <path> log --format="%ae" <range>`) against that repo's expected identity, if its config or CLAUDE.md names one. A machine's global git identity can be wrong for a repo it shares with other machines.

## Setup run from a side session lands the config on a side branch

**Seen:** 2026-11-18 (plantberg, commit abe3d90 on `claude/save-and-templates-e6209b`). Close-out ran in a side session: a worktree on its own branch, started by an orchestrator session that merges on the user's word. The repo had no `.claude/close-out.md`, so setup ran its full interview there. The new config was committed only to that side branch. Until the orchestrator merges it, other sessions (the main checkout, other side sessions) see no config and would run setup again, possibly with different answers.

**Proposal:** add to `setup.md`, before step 3 ("Ask"):

- If the run is in a worktree on a branch that isn't the repo's working branch (or the session was started by another session), say so before the first question. Recommend running setup from the main or orchestrator session instead, or carrying on with a note that the config only reaches other sessions once this branch merges.
- If setup goes ahead there, the closing report names the branch holding the config and tells the orchestrator (or parent session) to merge it, so no second setup runs in the meantime.
