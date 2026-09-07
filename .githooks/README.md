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
| `pre-push`   | Rejects a push when the Python files it carries are not formatted with `black` and `isort`, or when the test suite fails. |

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

Two stages run before a push is sent, and **both always run** — one push reports everything that is
wrong at once, instead of making you fix formatting, push again, and only then learn a test was
broken.

#### Stage 1 — formatting

Runs `black --check` and `isort --check-only`. The error names each offending file with a
copy-pasteable fix:

```bash
black <files>
isort <files>
```

**Only the `.py` files touched by the commits being pushed are checked** — not the whole repository.
The codebase is not fully formatted yet, so a repo-wide check would block every push; this way an
unrelated push is never blocked by someone else's old file, and the codebase converges to formatted
as files are touched.

Settings come from `pyproject.toml` in the repo root (line length 88, isort `profile = "black"`), so
the hook, the PyCharm External Tools and CI all agree. Without the shared `profile`, isort and black
disagree about multi-line imports and undo each other's work.

#### Stage 2 — tests

Runs `pytest -q` over the whole suite (unit, integration and architecture — about three seconds).
This stage is deliberately **not** scoped to the pushed files the way stage 1 is: a change in one
file can break a test anywhere, so scoping it would defeat the point.

pytest's own output is streamed rather than captured, so a failure reads exactly as it does when you
run the suite by hand.

The suite reads `POSTGRES_*` and `TOKEN_SECRET_KEY` through `load_dotenv()` in `app/config.py`, so a
clone without a `.env` fails wholesale. The hook says so when it sees no `.env`; fix it with
`cp .env.example .env`. (No database is involved — `tests/conftest.py` runs against in-memory
SQLite.)

#### Details worth knowing

- `black`, `isort` and `pytest` must be importable from the environment you push from — activate the
  project env first. If a tool is not found the push is rejected rather than silently skipped: a
  check that quietly disables itself is worse than no check.
- Both stages look at the files **as they exist on disk**, not as committed, which is what makes the
  reported paths directly fixable. If the working tree differs from `HEAD` the hook says so.
- Branch deletions and pushes with nothing new are silent no-ops — neither stage runs. A push that
  carries no `.py` files skips stage 1 but still runs the tests.

To bypass both stages for a single push (use sparingly): `git push --no-verify`.

Bypassing only defers the failure. Two workflows re-run the same checks on the remote — **Formatting**
(`.github/workflows/format.yml`) over the same file set, and **Tests**
(`.github/workflows/pytest.yml`) over the same suite — for every push and every PR into
`main`/`develop`. A skipped hook, or a clone that never ran the `core.hooksPath` command, turns into
a red check instead of a broken branch.
