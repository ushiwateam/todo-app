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
| `pre-push`   | Rejects a push when the Python files it carries are not formatted with `black` and `isort`.      |

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

### `pre-push`

Runs `black --check` and `isort --check-only` before a push is sent. Both always run, so one push
reports every problem at once, and the error names each offending file with a copy-pasteable fix:

```bash
black <files>
isort <files>
```

**Only the `.py` files touched by the commits being pushed are checked** — not the whole repository.
The codebase is not fully formatted yet, so a repo-wide check would block every push; this way an
unrelated push is never blocked by someone else's old file, and the codebase converges to formatted
as files are touched.

Settings come from `pyproject.toml` in the repo root (line length 88, isort `profile = "black"`), so
the hook, the PyCharm External Tools and any future CI all agree. Without the shared `profile`, isort
and black disagree about multi-line imports and undo each other's work.

`black` and `isort` must be importable from the environment you push from — activate the project env
first. If neither is found the push is rejected rather than silently skipped: a check that quietly
disables itself is worse than no check.

Two details worth knowing:

- Files are checked **as they exist on disk**, not as committed, which is what makes the reported
  paths directly fixable. If the working tree differs from `HEAD` the hook says so.
- Branch deletions, pushes carrying no `.py` files, and pushes with nothing new are all silent no-ops.

To bypass the hook for a single push (use sparingly): `git push --no-verify`.

Bypassing only defers the failure. The **Formatting** workflow (`.github/workflows/format.yml`) runs
the same two checks on the same file set for every push and every PR into `main`/`develop`, so a
skipped hook — or a clone that never ran the `core.hooksPath` command — turns into a red check
instead of unformatted code on the branch.
