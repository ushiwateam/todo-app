from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.dependencies import UserRepositoryDep
from app.responses import EMAIL_ALREADY_REGISTERED_RESPONSE, LOGIN_UNAUTHORIZED_RESPONSE
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import register, login, token_login

router = APIRouter(tags=["Users"])


@router.post(
    "/register",
    name="Register a new user",
    status_code=status.HTTP_201_CREATED,
    responses={
        **EMAIL_ALREADY_REGISTERED_RESPONSE
    }
)
def register_route(
        user: UserRegister,
        user_repository: UserRepositoryDep
):
    return register(user, user_repository)


@router.post("/login",
             name="Login an existent user",
             responses={
                 **LOGIN_UNAUTHORIZED_RESPONSE
             }
             )
def login_route(
        user: UserLogin,
        user_repository: UserRepositoryDep
):
    return login(user, user_repository)


@router.post("/token", include_in_schema=False)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repository: UserRepositoryDep
):
    return token_login(form_data, user_repository)
