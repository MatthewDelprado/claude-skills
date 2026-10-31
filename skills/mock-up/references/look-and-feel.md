# Finding the look and feel

A repo can declare one design system and use another, and migrations list both for months. Rank evidence by how close it is to the work, not by what the repo says about itself. Stop at the first step that settles it.

## Evidence order

1. **The work in front of you.** The file or route the user named, the files in `git diff` and `git status`, and what those files import.
2. **What the repo declares.** Design-system packages in `package.json`, Tailwind or theme config.
3. **Where the values live.** Token files, CSS variables, theme objects (`tokens.*`, `theme.*`, `:root` blocks, `tailwind.config.*`).
4. **How components are shaped.** Storybook stories, and two or three neighbouring components for markup, spacing and states.
5. **Neutral fallback.** Plain, restrained styling. Say clearly that nothing was found and this is a guess.

Steps 3 and 4 supply the values and markup shapes for the page, whichever system won in steps 1 and 2.

## Tie-break

When the nearby code genuinely mixes two systems, follow the migration direction:

- deprecation markers on one system's components or package
- migration notes, ADRs or a `MIGRATION.md`
- which package was added more recently (`git log -S"<package>" --format=%ad -- package.json | tail -1` gives the date it first appeared)

Pick the migration target. Always say which system you used and how to switch, even when you were confident.

## Override

A line in the repo's `CLAUDE.md` beats every step above:

```
mock-up: prefer <design system>
```

If a pick had to be flipped by the user, that is a feedback signal. Offer to log it, and suggest adding the override line.
