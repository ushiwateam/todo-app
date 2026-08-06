# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Run the app
- Docker (recommended, matches README): `docker compose up --build`
- Local: `uvicorn app.main:app --reload` (requires a running Postgres reachable via the `POSTGRES_*` env vars in `.env`)

### Database migrations (Alembic)
- Create migration after changing a SQLAlchemy model in `app/data_access/database/models/`: `alembic revision --autogenerate -m "description"`
- Apply: `alembic upgrade head`
- Rollback one: `alembic downgrade -1`
- Inside Docker: `docker compose exec app alembic upgrade head`

### Tests
- Run all: `pytest` (run from repo root; no pytest.ini/pyproject.toml — plain discovery under `tests/`)
- Unit only: `pytest tests/unit`
- Integration only: `pytest tests/integration`
- Architecture (layer-boundary) tests only: `pytest tests/architecture`
- Single test: `pytest tests/unit/application/services/test_todos.py::test_add_todo`
- Tests never touch the real Postgres DB — `tests/conftest.py` overrides the `get_db` dependency with an in-memory SQLite session (`StaticPool`, wrapped in a rollback-per-test transaction).
- Ignore `tests/Makefile` — it references a `features/...` test layout that no longer exists after the layered-architecture refactor.
- CI: `.github/workflows/pytest.yml` runs `pytest` on push and on PRs into `main`.

## Architecture

This is a **layered architecture**, refactored from a flat FastAPI layout into three layers under `app/`. Each layer only knows about the layer(s) below it through interfaces, never concrete implementations:

```
presentation/  → business/  → data_access/
(routers,        (services,     (repositories,
 schemas)         interfaces,    interfaces,
                   entities,      mappers,
                   exceptions)    db models)
```

- **`app/business/`** — the domain/application layer.
  - `entities/` — plain `@dataclass(slots=True)` domain objects (`Todo`, `User`), independent of both the SQLAlchemy models and the Pydantic API schemas.
  - `interfaces/` — abstract base classes (`ITodoService`, `IAuthService`) that services implement; routers depend on these interfaces via FastAPI `Depends`, not concrete classes.
  - `services/` — business logic (`TodoService`, `AuthService`). A service is constructed per-request with its repository (and, for `TodoService`, the current authenticated user) injected — see `app/dependencies.py`.
  - `exceptions/` — domain errors (`TodoNotFoundError`, `UnauthorizedAccessError`, `EmailAlreadyRegisteredError`, `InvalidCredentialsError`), all subclassing `BusinessError` in `app/exceptions.py`.

- **`app/data_access/`** — persistence layer.
  - `database/models/` — the actual SQLAlchemy ORM models (`User`, `Todo`), separate from business entities.
  - `database/session.py` — engine/`SessionLocal` built from `POSTGRES_*` env vars (`app/config.py`).
  - `interfaces/` — repository contracts (`ITodoRepository`, `IUserRepository`).
  - `mappers/` — pure functions converting between business entities and SQLAlchemy models (`to_entity` / `to_model`), so services never see ORM objects directly.
  - `repositories/base.py` — generic `ISqlAlchemyRepository[TEntity, TModel]` with shared CRUD helpers (`_create`, `_get_one_or_none`, `get_all`, `_update`, `_delete`); concrete repositories (`TodoSqlAlchemyRepository`, `UserSqlAlchemyRepository`) subclass this and supply `to_model`/`to_entity`.

- **`app/presentation/`** — HTTP layer.
  - `routers/` — FastAPI route handlers (`auth.py`: `/register`, `/login`, `/token`; `todos.py`: CRUD under `/todos`). Handlers call into a service obtained via `Depends`, then translate business exceptions into `HTTPException`s (e.g. `TodoNotFoundError` → 404, `UnauthorizedAccessError` → 403).
  - `schemas/` — Pydantic request/response models, distinct from both business entities and DB models.
  - `error_responses.py` — shared OpenAPI `responses={}` dicts (e.g. `NOT_FOUND_RESPONSE`, `FORBIDDEN_RESPONSE`) attached to router decorators for accurate Swagger docs.

- **Dependency wiring** (`app/dependencies.py`) is the composition root: it defines `get_db`, `get_current_user` (JWT decode + DB lookup), and factory functions (`get_todo_repository`, `get_todo_service`, etc.) exposed as `Annotated[...]` `*Dep` aliases (`TodoServiceDep`, `AuthServiceDep`, `CurrentUserDep`, ...) that routers depend on. This is the one place that wires interfaces to concrete implementations — start here when tracing how a request reaches a service. **Known leaks in `get_current_user`**, both documented as currently-failing tests in `tests/unit/test_dependencies.py`, neither fixed yet: (1) it imports `User` from `app.data_access.database.models.user` (the ORM model) and returns the raw ORM row unmapped, so `CurrentUserDep`/`get_todo_service` pass an ORM `User` into `TodoService`, even though `ITodoService.__init__` (`app/business/interfaces/todo.py`) declares `user: User` as the business entity from `app.business.entities.user` (`test_get_current_user_returns_business_entity`); (2) it depends on a raw `Session` (`db: DbDep`) and calls `db.execute(select(User)...)` directly instead of going through `IUserRepository` like every other persistence access in the codebase — `IUserRepository` doesn't even have a `get_user_by_id` method yet (`test_get_current_user_should_not_depend_on_raw_db_session`).

- **Error model** (`app/exceptions.py`): all domain errors derive from `AppError`, split into `PresentationError` / `DataAccessError` / `BusinessError` base classes. Routers currently only catch specific `BusinessError` subclasses per-endpoint (no global exception handler yet).

- **Auth** (`app/security.py`): bcrypt password hashing via `passlib`, JWT creation via `python-jose`. `AuthService.authenticate_user` runs `pwd_context.verify` against a `DUMMY_HASH` even when the user doesn't exist, to keep login timing constant regardless of whether the email exists.

- **Note on README.md**: its "Project Structure" section describes the pre-refactor flat layout (`app/models/`, `app/schemas/`, `app/routers/`, `app/services/`) and is out of date — the layered structure above (also mirrored in `architecture.txt`) is what's actually in the repo.

- **Architecture tests** (`tests/architecture/test_layer_boundaries.py`) use `pytest-archon` to enforce the layer boundaries described above at the import level (e.g. `presentation` can't import `data_access` directly, `business` can't import concrete `data_access` internals, nothing imports `presentation` from below). They check direct imports only (`only_direct_imports=True`) — the composition root `app/dependencies.py` intentionally imports across all layers to wire things up, so transitive-import checking would produce false positives there. A separate rule (`test_business_should_not_import_web_framework`) asserts `app/business*` never imports FastAPI/Flask/Starlette/Django directly, since business logic is meant to be framework-agnostic — this rule currently **fails**, because `app/business/interfaces/auth.py` and `app/business/services/auth_service.py` both import `fastapi.security.OAuth2PasswordRequestForm` for `token_login`; that's a known, not-yet-fixed leak.
