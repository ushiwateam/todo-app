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
todo-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment variables configuration (pydantic-settings)
│   ├── database.py          # SQLAlchemy database connection
│   ├── models/
│   │   ├── user.py          # User SQLAlchemy model
│   │   └── todo.py          # Todo SQLAlchemy model
│   ├── schemas/
│   │   ├── user.py          # Pydantic schemas (request/response)
│   │   └── todo.py
│   ├── routers/
│   │   ├── auth.py          # /register, /login endpoints
│   │   └── todos.py         # /todos CRUD endpoints
│   ├── services/
│   │   ├── auth_service.py  # Authentication business logic
│   │   └── todo_service.py  # Todo business logic
│   └── dependencies.py      # get_current_user, get_db dependencies
├── alembic/                 # Database migrations
├── tests/
│   ├── test_auth.py
│   └── test_todos.py
├── .env                     # Local environment variables (never committed)
├── .env.example             # Environment variables template
├── .gitignore
├── docker-compose.yml       # API + PostgreSQL services
├── Dockerfile
└── requirements.txt
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
cd todo-api
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

---

## 🌿 Git Workflow

### Branches

```text
main
develop
feature/<feature-name>
```

### Conventional Commits

```text
feat: add user registration endpoint
feat: implement JWT authentication
fix: handle duplicate email validation
docs: update README
test: add authentication tests
```

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
