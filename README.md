# 📋 Todo API

A RESTful Todo API built with FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication.


---

## 🚀 Features

* User registration and login
* JWT authentication
* CRUD operations for todos
* Pagination support
* PostgreSQL persistence
* Alembic migrations
* Dockerized environment
* Automated tests

---

## 🛠️ Tech Stack

| Component        | Technology              |
| ---------------- | ----------------------- |
| Language         | Python 3.11+            |
| API Framework    | FastAPI                 |
| Database         | PostgreSQL              |
| ORM              | SQLAlchemy              |
| Migrations       | Alembic                 |
| Authentication   | JWT (python-jose)       |
| Testing          | pytest + httpx          |
| Containerization | Docker + Docker Compose |

---

## 📁 Project Structure

```text
todo-app/
├── app/
│   ├── main.py                     # FastAPI application entry point
│   ├── config.py                   # Environment variables (POSTGRES_*, TOKEN_SECRET_KEY)
│   ├── security.py                 # Password hashing + JWT encode/decode
│   ├── exceptions.py               # AppError base classes
│   ├── dependencies.py             # Composition root: get_db, get_current_user, *Dep aliases
│   │
│   ├── auth/                       # ── feature slice: users, registration, login ──
│   │   ├── business/
│   │   │   ├── entity.py           # User domain entity (dataclass)
│   │   │   ├── interface.py        # IAuthService
│   │   │   ├── service.py          # AuthService
│   │   │   └── exceptions.py       # EmailAlreadyRegisteredError, InvalidCredentialsError
│   │   ├── data_access/
│   │   │   ├── interface.py        # IUserRepository
│   │   │   ├── repository.py       # UserSqlAlchemyRepository
│   │   │   ├── mapper.py           # entity <-> model
│   │   │   └── model.py            # User SQLAlchemy model
│   │   └── presentation/
│   │       ├── router.py           # /register, /login, /token
│   │       └── schemas.py          # Pydantic request/response models
│   │
│   ├── todos/                      # ── feature slice: todo CRUD (same three layers) ──
│   │   ├── business/               # entity.py, interface.py, service.py, exceptions.py
│   │   ├── data_access/            # interface.py, repository.py, mapper.py, model.py
│   │   └── presentation/           # router.py (/todos), schema.py
│   │
│   └── shared/                     # ── what both slices build on ──
│       ├── database/
│       │   ├── base.py             # SQLAlchemy DeclarativeBase
│       │   └── session.py          # Engine + SessionLocal
│       ├── data_access/
│       │   └── base_repository.py  # Generic ISqlAlchemyRepository
│       └── presentation/
│           ├── error_responses.py  # Shared OpenAPI responses={} dicts
│           └── errors_schemas.py   # ErrorResponse schema
│
├── alembic/                        # Database migrations
├── tests/
│   ├── conftest.py                 # In-memory SQLite session, TestClient fixtures
│   ├── unit/
│   ├── integration/
│   └── architecture/               # pytest-archon boundary rules
├── .githooks/                      # commit-msg + pre-push hooks
├── .env                            # Local environment variables (never committed)
├── .env.example                    # Environment variables template
├── docker-compose.yml              # API + PostgreSQL services
├── Dockerfile
├── pyproject.toml                  # black + isort settings
├── requirements.txt
└── requirements-dev.txt            # Pinned black + isort
```

---

## 📦 Prerequisites

Make sure the following tools are installed:

* Docker
* Docker Compose
* Git

---

## ⚙️ Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Example:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=todo_db
POSTGRES_PORT=5432
POSTGRES_HOST=db

TOKEN_SECRET_KEY=your-secret-key
```


---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/ushiwateam/todo-app.git
cd todo-app
```

### 2. Configure environment variables

Update the `.env` file according to your environment.

### 3. Start the application

Build and start all services:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d
```

### 4. Apply database migrations

```bash
docker compose exec app alembic upgrade head
```

### 5. Access the API

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

### Useful Commands

Stop services:

```bash
docker compose down
```

View API logs:

```bash
docker compose logs -f app
```

---

## 🗄️ Database Migrations

This project uses **Alembic** to manage database schema changes and versioning.

### Create a New Migration

After modifying your SQLAlchemy models:

```bash
alembic revision --autogenerate -m "add todo status column"
```

### Apply Migrations

Run all pending migrations:

```bash
alembic upgrade head
```

### Roll Back One Migration

```bash
alembic downgrade -1
```

### View Current Migration Version

```bash
alembic current
```

### View Migration History

```bash
alembic history
```

### Running Migrations Inside Docker

```bash
docker compose exec app alembic upgrade head
```

### Notes

* Never modify the database schema manually.
* All schema changes must be tracked through Alembic migrations.
* Migration files are stored in the `alembic/versions/` directory.
* Keep migrations small and focused on a single schema change.

---

## 🔐 Authentication

All todo endpoints require a valid JWT token.

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## 🛣️ API Endpoints

### Authentication

| Method | Endpoint    | Description         |
| ------ | ----------- | ------------------- |
| POST   | `/register` | Register a new user |
| POST   | `/login`    | Authenticate a user |

### Todos

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| POST   | `/todos`      | Create a todo           |
| GET    | `/todos`      | List user todos         |
| PUT    | `/todos/{id}` | Replace a todo          |
| PATCH  | `/todos/{id}` | Partially update a todo |
| DELETE | `/todos/{id}` | Delete a todo           |

---

## 💡 Example Request

Create a todo:

```bash
curl -X POST http://localhost:8000/todos \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
  "title": "Learn FastAPI",
  "description": "Build a Todo API"
}'
```

---

## 🧪 Testing

Run tests locally:

```bash
pytest
```

Run tests inside Docker:

```bash
docker compose exec app pytest
```

The suite has three tiers:

```bash
pytest tests/unit           # Services in isolation, repositories faked
pytest tests/integration    # Routers end to end through a TestClient
pytest tests/architecture   # Import-boundary rules between slices and layers
```

Tests never touch the real PostgreSQL database — `tests/conftest.py` overrides the `get_db`
dependency with an in-memory SQLite session, rolled back after every test.

---

## 🏗️ Architecture

```text
Client
   │
   ▼
FastAPI API
   │
   ▼
PostgreSQL
```

Docker Compose orchestrates both services locally.

### Feature-based structure

The code is organised **by feature (vertical slices)** rather than by technical layer. Each slice
(`app/auth/`, `app/todos/`) owns its own three layers, so everything a feature needs lives in one
directory:

```text
<feature>/presentation/  →  <feature>/business/  →  <feature>/data_access/
(router, schemas)           (service, interface,     (repository, interface,
                             entity, exceptions)      mapper, ORM model)
```

Dependencies point one way only, and every layer reaches the one below it through an interface
rather than a concrete class. `app/shared/` holds what both slices build on (the declarative `Base`,
the session factory, the generic `ISqlAlchemyRepository`, the shared OpenAPI error responses) and
never imports a feature. `app/dependencies.py` is the composition root — the single place that binds
interfaces to implementations, and the only module that imports across every slice.

Because file names are positional (`interface.py` is "the interface of *this* layer of *this*
feature"), `app/auth/business/interface.py` is `IAuthService` while `app/auth/data_access/interface.py`
is `IUserRepository`.

Slices stay independent: `auth` must not import `todos` at all, and `todos` may use only the `auth`
business entity (it owns a `user_id`), never auth's service, repository, mapper, ORM model or router.
These rules are not conventions on paper — `tests/architecture/test_layer_boundaries.py` enforces
them with [pytest-archon](https://github.com/jwbargsten/pytest-archon), so a boundary violation fails
the test suite.

---

## 🌿 Git Workflow

### Branches

```text
main
develop
feature/<feature-name>
```

### Conventional Commits

Commit messages follow [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
and are **enforced by a `commit-msg` git hook** (`.githooks/commit-msg`). Enable it once per clone:

```bash
git config core.hooksPath .githooks
```

Format:

```text
<type>[optional scope][!]: <description>

[optional body, after one blank line]

[optional footer(s), after one blank line]
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`,
`revert`.

```text
feat: add user registration endpoint
feat: implement JWT authentication
fix(auth): handle duplicate email validation
feat(api)!: drop v1 todo payload
docs: update README
test: add authentication tests
```

A message that doesn't match is rejected with an explanation, and the commit is aborted. The typed
message is preserved — recover it with `git commit -e -F .git/COMMIT_EDITMSG`.

### Formatting

Python code is formatted with [black](https://black.readthedocs.io/) and
[isort](https://pycqa.github.io/isort/). Settings live in `pyproject.toml` — line length 88 and
isort `profile = "black"`, so the two tools agree on multi-line imports.

```bash
pip install -r requirements-dev.txt   # pinned black + isort
black <files>
isort <files>
```

This is **enforced by a `pre-push` git hook** (`.githooks/pre-push`), activated by the same
`git config core.hooksPath .githooks` as above. It checks only the `.py` files carried by the commits
being pushed and rejects the push if any of them is unformatted, naming the files and the fix
command. Bypass a single push with `git push --no-verify`.

The hook is local, so it can be skipped — a `--no-verify` push, or a clone that never ran the
`core.hooksPath` command. The **Formatting** GitHub Actions workflow
(`.github/workflows/format.yml`) is the backstop: it re-runs the same two checks on the same file
set for every push and every PR into `main`/`develop`, annotates the offending lines in the diff and
prints the fix in the run summary. Bypassing the hook only defers the failure to CI.

---

## 🚧 Roadmap

* Todo status management
* Filtering and sorting
* Refresh tokens
* Rate limiting
* GitHub Actions CI/CD

---

## 📜 License

This project is intended for educational and portfolio purposes.
