# Git hooks

Versioned git hooks for this repository. Git cannot track `.git/hooks/` itself, so the hooks live
here and are activated by pointing git at this directory.

## Enable (once per clone)

```bash
git config core.hooksPath .githooks
```

## Hooks

| Hook         | What it does                                                                                   |
| ------------ | ---------------------------------------------------------------------------------------------- |
| `commit-msg` | Rejects commit messages that don't follow [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Valid messages commit normally. |

### `commit-msg`

Required format:

```text
<type>[optional scope][!]: <description>

[optional body, after one blank line]

[optional footer(s), after one blank line]
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`,
`revert`.

Merge, revert, `fixup!` and `squash!` messages are skipped so `git merge` and `git rebase` keep
working.

If a commit is rejected the message is not lost — recover and edit it with:

```bash
git commit -e -F .git/COMMIT_EDITMSG
```

To bypass the hook for a single commit (use sparingly): `git commit --no-verify`.
