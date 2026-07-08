from datetime import timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import UserRepositoryDep
from app.schemas.user import UserRegister, UserLogin
from app.config import ACCESS_TOKEN_EXPIRE_HOURS
from app.utils import create_access_token, prepare_token_data, pwd_context

DUMMY_HASH = pwd_context.hash("dummypassword")


def register(user_data: UserRegister, user_repository: UserRepositoryDep):
    existing_user = user_repository.get_user_by_email(user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user_data.password)

    user = user_repository.create_user(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    token_data = prepare_token_data(user)
    token = create_access_token(token_data, access_token_expires)
    return {"token": token}


def authenticate_user(email, password, user_repository: UserRepositoryDep):
    existing_user = user_repository.get_user_by_email(email)
    if not existing_user:
        pwd_context.verify(password, DUMMY_HASH)
        return None
    if not pwd_context.verify(password, existing_user.password):
        return None
    return existing_user


def login(user_data: UserLogin, user_repository: UserRepositoryDep):
    existing_user = authenticate_user(user_data.email, user_data.password, user_repository)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email inexistant ou mot de passe incorrect"
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    token_data = prepare_token_data(existing_user)
    token = create_access_token(token_data, access_token_expires)
    return {"token": token}


def token_login(form_data: OAuth2PasswordRequestForm, user_repository: UserRepositoryDep):
    existing_user = authenticate_user(form_data.username, form_data.password, user_repository)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email inexistant ou mot de passe incorrect"
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    token_data = prepare_token_data(existing_user)
    token = create_access_token(token_data, access_token_expires)
    return {"access_token": token, "token_type": "bearer"}
