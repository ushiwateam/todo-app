from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.features.auth.application.utils import pwd_context, create_access_token, prepare_token_data
from app.config import ACCESS_TOKEN_EXPIRE_HOURS
from app.dependencies import get_db
from app.features.auth.infrastrcuture.model import User
from app.features.todos.infrastructure.model import Todo
from app.main import app
from app.shared.database.session import Base

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
def init_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def create_user(db):
    def _create_user(**kwargs):
        user = User(
            name=kwargs.get("name", "Test User"),
            email=kwargs.get("email", "test@example.com"),
            password=pwd_context.hash(kwargs.get("password", "dummypassword")),
        )

        db.add(user)
        db.flush()

        return user

    return _create_user


@pytest.fixture
def create_todo(db):
    def _create_todo(user: User, **kwargs):
        todo = Todo(
            title=kwargs.get("title", "Test title"),
            description=kwargs.get("description", "dummy description"),
            user_id=user.id
        )

        db.add(todo)
        db.flush()

        return todo

    return _create_todo


@pytest.fixture
def auth_headers():
    def _auth_headers(user: User):
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        token = create_access_token(prepare_token_data(user), access_token_expires)
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers


@pytest.fixture
def create_user_entity():
    def _create_user(**kwargs) -> User:
        defaults = {
            "id": 1,
            "name": "user",
            "email": "user@example.com",
            "password": "password",
        }

        return User(**(defaults | kwargs))

    return _create_user
