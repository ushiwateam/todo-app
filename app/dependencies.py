from typing import Annotated

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.config import TOKEN_SECRET_KEY, TOKEN_ALGORITHM
from app.database import SessionLocal
from app.models.user import User
from app.repositories import UserRepository, TodoRepository
from app.services.auth_service import AuthService
from app.services.todo_service import TodoService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

DbDep = Annotated[Session, Depends(get_db)]


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email inexistant ou mot de passe incorrect"
    )
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    existing_user = db.execute(select(User).where(
        User.id == int(user_id),
        User.email == payload.get("email")
    )).scalar_one_or_none()
    if existing_user is None:
        raise credentials_exception
    return existing_user

def get_user_repository(db: DbDep):
    return UserRepository(db)

def get_todo_repository(db: DbDep):
    return TodoRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
TodoRepositoryDep = Annotated[TodoRepository, Depends(get_todo_repository)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]

def get_todo_service(todo_repository: TodoRepositoryDep, user: CurrentUserDep):
    return TodoService(todo_repository, user)

TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]

def get_auth_service(user_repository: UserRepositoryDep):
    return AuthService(user_repository)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
