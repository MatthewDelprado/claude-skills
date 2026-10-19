# close-out — improvement proposals

Proposals from Step 6 runs. Each `## ` heading is one theme; add new evidence to an existing theme rather than opening a duplicate (see Step 6's dedupe rule).

## Work done in another repo or a scratch clone isn't checked

**Seen:** 2026-10-19. The session's real work was in a different repo from the one close-out ran in, edited through a temporary clone in the session's scratchpad. Step 1 only inspects the current repo, so it reported a clean tree with nothing to land, and none of the steps looked at the other repo. The scratch clone was also wiped when the session restarted partway through, so a commit left there unpushed would have been lost without any warning.

**Proposal:** add to Step 1:

- List every repo this session wrote to (from the conversation: `git -C <path>` commands, clones, `gh` PRs against another `--repo`), not only the current one.
- For each one, check for uncommitted changes, unpushed commits (`git -C <path> status -sb`), and branches or PRs the session opened that are still open. Report each, and treat work held only in a scratch or temp directory as at risk.
- Check the author email on this session's commits in each repo (`git -C <path> log --format="%ae" <range>`) against that repo's expected identity, if its config or CLAUDE.md names one. A machine's global git identity can be wrong for a repo it shares with other machines.
