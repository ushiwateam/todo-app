from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.business.entities import User
from app.business.interfaces.auth import IAuthService
from app.business.interfaces.todo import ITodoService
from app.data_access.interfaces.todo import ITodoRepository
from app.data_access.interfaces.user import IUserRepository
from app.data_access.database.session import SessionLocal
from app.data_access.repositories.user_repository import UserSqlAlchemyRepository
from app.data_access.repositories.todo_repository import TodoSqlAlchemyRepository
from app.business.services.auth_service import AuthService
from app.business.services.todo_service import TodoService

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


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_service: AuthServiceDep):
    return user_service.get_current_user(token)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_todo_service(todo_repository: TodoRepositoryDep, user: CurrentUserDep) -> ITodoService:
    return TodoService(todo_repository, user)


TodoServiceDep = Annotated[ITodoService, Depends(get_todo_service)]
