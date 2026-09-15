# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Run the app
- Docker (recommended, matches README): `docker compose up --build`
- Local: `uvicorn app.main:app --reload` (requires a running Postgres reachable via the `POSTGRES_*` env vars in `.env`)

### Database migrations (Alembic)
- Create migration after changing a SQLAlchemy model (`app/auth/data_access/model.py`, `app/todos/data_access/model.py`): `alembic revision --autogenerate -m "description"`
- Apply: `alembic upgrade head`
- Rollback one: `alembic downgrade -1`
- Inside Docker: `docker compose exec app alembic upgrade head`

### Tests
- Run all: `pytest` (run from repo root; `pyproject.toml` has no `[tool.pytest.ini_options]`, so this is plain discovery under `tests/`)
- Unit only: `pytest tests/unit`
- Integration only: `pytest tests/integration`
- Architecture (feature- and layer-boundary) tests only: `pytest tests/architecture`
- Single test: `pytest tests/unit/application/services/test_todos.py::test_add_todo`
- Tests never touch the real Postgres DB — `tests/conftest.py` overrides the `get_db` dependency with an in-memory SQLite session (`StaticPool`, wrapped in a rollback-per-test transaction).
- Ignore `tests/Makefile` — it references a test layout that predates the current one.
- `tests/` mirrors the *old* layered layout (`tests/unit/application/services/`, `tests/integration/presentation/`) rather than the feature slices. The imports are correct; only the directory names lag behind. Moving them to `tests/auth/` + `tests/todos/` is a reasonable follow-up, not a bug.
- CI: `.github/workflows/pytest.yml` runs `pytest` on push and on PRs into `main` or `develop`.

### CI workflows
- `.github/workflows/pytest.yml` — `pytest` on every push and on PRs into `main`/`develop`.
- `.github/workflows/format.yml` ("Formatting") — the server-side backstop for the `pre-push` hook, which is local and bypassable (`--no-verify`, or any clone that never ran `git config core.hooksPath .githooks`). It resolves the changed `.py` files (PR → `merge-base(base, head)`; push → `github.event.before`, falling back to `merge-base` with `origin/develop` then `origin/main` when `before` is all zeros on a new branch), then runs `black --check --diff` and `isort --check-only --diff` over exactly that set. Both tools always run; failures become `::error file=` annotations plus a `$GITHUB_STEP_SUMMARY` with the fix. **Note the fallback order matters** — `main` is stale (`c86ff2f`), so a merge-base against it would drag in most of the repo; `origin/develop` is the real trunk.
- The formatting job scopes itself to changed files for the same reason the hook does (see the note below about the repo not being clean). Zero changed `.py` files → the job passes without running the tools.
- Formatter versions are pinned in `requirements-dev.txt` (`black==26.5.1`, `isort==8.0.1`), deliberately separate from `requirements.txt` because the `Dockerfile` installs that one into the runtime image. Bump both together with the local env, or CI and developers will disagree about what "formatted" means.
- A red check does not block a merge on its own — **Formatting** must be added as a required status check in branch protection for `main`/`develop` for it to actually gate merges.

### Git hooks
- `.githooks/commit-msg` enforces [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) on every commit (POSIX sh, no dependencies). Allowed types: `feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert` — note `feature:`, used in older commits, is **not** accepted.
- `.githooks/pre-push` (also POSIX sh, no dependencies) runs **two stages**, and both always run so one push reports everything at once; the verdict is printed once at the end.
  - **Stage 1 — formatting**: `black --check` and `isort --check-only` on the `.py` files carried by the commits being pushed, rejecting the push if any is unformatted. It reads the ref lines git supplies on stdin: a new branch (`remote_sha` all zeros) resolves to `git rev-list <local> --not --remotes=<remote>` plus a `git diff-tree --root` per commit, otherwise `git diff <remote_sha> <local_sha>`; results are filtered to `.py` paths that still exist on disk. A push carrying no `.py` files skips this stage.
  - **Stage 2 — tests**: `pytest -q` over the whole suite, run from the repo root. Deliberately *not* scoped to the pushed files the way stage 1 is — a change in one file can break a test anywhere, and the suite is ~3s. Output is streamed, not captured, so failures read as they do by hand. The suite needs `POSTGRES_*`/`TOKEN_SECRET_KEY` (via `load_dotenv()` in `app/config.py`), so the hook adds a `cp .env.example .env` hint when it finds no `.env`.
  - A ref-line loop flag (`HAS_REFS`) makes a pure branch deletion exit before either stage. A missing `black`/`isort`/`pytest` is a hard failure rather than a silent skip. Bypass both stages with `git push --no-verify` — `.github/workflows/pytest.yml` is the backstop for the test stage exactly as `format.yml` is for the format stage.
- Formatter settings live in `pyproject.toml` (`line-length = 88`, isort `profile = "black"`) — the one place shared by the hook, the PyCharm External Tools and any future CI. It contains no `[tool.pytest.ini_options]`, so test discovery is unaffected — pytest prints `configfile: pyproject.toml`, but rootdir, collection and results are identical (35 collected, 35 passed with and without the file).
- **The repo is not yet black/isort-clean** (33 of 55 `.py` files fail black; isort is in a similar state). The feature-based refactor did not change this — it moved files, it did not reformat them. That is why `pre-push` is scoped to pushed files instead of the whole repo — a repo-wide check would block every push until a bulk reformat lands. Don't add a repo-wide `black --check .` to CI before that reformat happens.
- Activate once per clone: `git config core.hooksPath .githooks`. Git can't version `.git/hooks/`, so hooks live in `.githooks/` and this config points at them.
- Merge/revert/`fixup!`/`squash!` messages are skipped. Bypass for one commit with `git commit --no-verify`.

## Architecture

This is a **feature-based (vertical slice) architecture**, refactored from the earlier three-layer layout (`app/business/`, `app/data_access/`, `app/presentation/` — those packages no longer exist). The top-level split is now by feature; the three layers still exist, but *inside* each feature:

```
app/
├── auth/                   # slice: users, registration, login, JWT
│   ├── business/           entity.py  interface.py  service.py  exceptions.py
│   ├── data_access/        interface.py  repository.py  mapper.py  model.py
│   └── presentation/       router.py  schemas.py
├── todos/                  # slice: todo CRUD — same three layers, same file names
│   ├── business/           entity.py  interface.py  service.py  exceptions.py
│   ├── data_access/        interface.py  repository.py  mapper.py  model.py
│   └── presentation/       router.py  schema.py
├── shared/                 # what both slices are built on
│   ├── database/           base.py (DeclarativeBase)  session.py (engine/SessionLocal)
│   ├── data_access/        base_repository.py (ISqlAlchemyRepository)
│   └── presentation/       error_responses.py  errors_schemas.py
├── dependencies.py         # composition root — the only cross-everything module
├── config.py  security.py  exceptions.py  main.py
```

Within a slice the dependency direction is the same as before — `presentation → business → data_access`, each layer reaching the one below only through interfaces, never concrete implementations:

```
<feature>/presentation/  → <feature>/business/  → <feature>/data_access/
(router, schemas)          (service, interface,    (repository, interface,
                            entity, exceptions)     mapper, ORM model)
```

**The file naming is positional, not descriptive** — `interface.py` means "the interface of *this* layer of *this* feature". So `app/auth/business/interface.py` is `IAuthService` while `app/auth/data_access/interface.py` is `IUserRepository`. When tracing an import, read the directory, not just the filename.

- **`<feature>/business/`** — the domain layer.
  - `entity.py` — a plain `@dataclass(slots=True)` domain object (`Todo`, `User`), independent of both the SQLAlchemy model and the Pydantic schemas.
  - `interface.py` — the abstract service base class (`ITodoService`, `IAuthService`); routers depend on these via FastAPI `Depends`, not on the concrete class.
  - `service.py` — business logic (`TodoService`, `AuthService`), constructed per-request with its repository (and, for `TodoService`, the current authenticated user) injected — see `app/dependencies.py`.
  - `exceptions.py` — domain errors (`TodoNotFoundError`, `UnauthorizedAccessError`, `EmailAlreadyRegisteredError`, `InvalidCredentialsError`), all subclassing `BusinessError` in `app/exceptions.py`.

- **`<feature>/data_access/`** — the persistence layer.
  - `model.py` — the SQLAlchemy ORM model, separate from the business entity.
  - `interface.py` — the repository contract (`ITodoRepository`, `IUserRepository`).
  - `mapper.py` — pure `to_entity` / `to_model` functions, so services never see ORM objects.
  - `repository.py` — the concrete repository, subclassing `ISqlAlchemyRepository` from `app/shared/data_access/base_repository.py` and supplying `to_model`/`to_entity`.

- **`<feature>/presentation/`** — the HTTP layer.
  - `router.py` — FastAPI handlers (`auth`: `/register`, `/login`, `/token`; `todos`: CRUD under `/todos`). Handlers call a service obtained via `Depends`, then translate business exceptions into `HTTPException`s (`TodoNotFoundError` → 404, `UnauthorizedAccessError` → 403).
  - `schemas.py` / `schema.py` — Pydantic request/response models, distinct from both entities and ORM models. (The two slices spell this one differently; `todos` uses the singular.)

- **`app/shared/`** — what both slices sit on: `ISqlAlchemyRepository[TEntity, TModel]` with its CRUD helpers (`_create`, `_get_one_or_none`, `get_all`, `_update`, `_delete`), the declarative `Base`, the engine/`SessionLocal` built from `POSTGRES_*` env vars, and the shared OpenAPI `responses={}` dicts (`NOT_FOUND_RESPONSE`, `FORBIDDEN_RESPONSE`, …) attached to router decorators. **`shared` never imports a feature** — the dependency only ever points feature → shared.

- **Cross-feature rules.** `auth` is the lower slice and must not know `todos` exists at all. `todos` may import `app.auth.business.entity` (it owns a `user_id` and `ITodoService` is typed against the `User` entity) but nothing else of auth's — not its service, repository, mapper, ORM model, router or schemas. A slice's public surface is its business entity and its interfaces; everything else is private to it. Both rules are enforced by `tests/architecture/test_layer_boundaries.py`.
  - The one deliberate exception is `app/security.py`, which imports `app.auth.data_access.model.User` purely as a type hint for `prepare_token_data`. It's shared code reaching into a feature — acceptable while auth is the only thing that mints tokens, worth revisiting if a second slice needs them.

- **Dependency wiring** (`app/dependencies.py`) is the composition root: `get_db`, `get_current_user`, and the factory functions (`get_todo_repository`, `get_todo_service`, …) exposed as `Annotated[...]` `*Dep` aliases (`TodoServiceDep`, `AuthServiceDep`, `CurrentUserDep`, …) that routers depend on. This is the one place that wires interfaces to concrete implementations, and the one module that legitimately imports across every slice and layer — start here when tracing how a request reaches a service. The `get_current_user` leaks documented in earlier revisions of this file are **fixed**: it now delegates to `AuthServiceDep` (`AuthService.get_current_user` decodes the JWT and loads the user through `IUserRepository.get_user_by_id`), so it neither touches a raw `Session` nor returns an unmapped ORM row. `tests/unit/test_dependencies.py` keeps the raw-session assertion as a regression guard, and it passes.

- **Error model** (`app/exceptions.py`): all domain errors derive from `AppError`, split into `PresentationError` / `DataAccessError` / `BusinessError` base classes. Routers only catch specific `BusinessError` subclasses per-endpoint (no global exception handler yet).

- **Auth** (`app/security.py`): bcrypt password hashing via `passlib`, JWT creation via `python-jose`. `AuthService.authenticate_user` runs `pwd_context.verify` against a `DUMMY_HASH` even when the user doesn't exist, to keep login timing constant regardless of whether the email exists.

- **Architecture tests** (`tests/architecture/test_layer_boundaries.py`) use `pytest-archon` to enforce all of the above at the import level: the two cross-feature rules, `shared` not importing features, and the per-slice layering (presentation ↛ data_access, business ↛ presentation, business ↛ ORM/repository/mapper, data_access ↛ presentation or business services/interfaces). Patterns are written as `app.*.presentation*` / `app.*.business*` / `app.*.data_access*` so they cover both slices. They check direct imports only (`only_direct_imports=True`) — `app/dependencies.py` intentionally imports across every boundary to wire things up, so transitive checking would flag any router that imports it. A separate rule (`test_business_should_not_import_web_framework`) asserts no business module imports FastAPI/Flask/Starlette/Django; unlike in the layered layout, this rule now **passes** — the `OAuth2PasswordRequestForm` leak is gone, `token_login` takes plain `email`/`password` and the form binding lives in `FormDataDep` in the composition root.
  - A rule whose `.match()` pattern selects no modules passes vacuously. If you rename a package, re-check these patterns still match something — that is exactly how the old layer rules went silently dead after this refactor.
