from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.business.entity import User
from app.auth.business.interface import IAuthService
from app.auth.business.service import AuthService
from app.auth.data_access.interface import IUserRepository
from app.auth.data_access.repository import UserSqlAlchemyRepository
from app.shared.database.session import SessionLocal
from app.todos.business.interface import ITodoService
from app.todos.business.service import TodoService
from app.todos.data_access.interface import ITodoRepository
from app.todos.data_access.repository import TodoSqlAlchemyRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


DbDep = Annotated[Session, Depends(get_db)]


def get_user_repository(db: DbDep):
    return UserSqlAlchemyRepository(db)


def get_todo_repository(db: DbDep):
    return TodoSqlAlchemyRepository(db)


UserRepositoryDep = Annotated[IUserRepository, Depends(get_user_repository)]
TodoRepositoryDep = Annotated[ITodoRepository, Depends(get_todo_repository)]
FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_auth_service(user_repository: UserRepositoryDep) -> IAuthService:
    return AuthService(user_repository)


AuthServiceDep = Annotated[IAuthService, Depends(get_auth_service)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], user_service: AuthServiceDep
):
    return user_service.get_current_user(token)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_todo_service(
    todo_repository: TodoRepositoryDep, user: CurrentUserDep
) -> ITodoService:
    return TodoService(todo_repository, user)


TodoServiceDep = Annotated[ITodoService, Depends(get_todo_service)]
