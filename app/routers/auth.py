from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.dependencies import UserRepositoryDep
from app.responses import EMAIL_ALREADY_REGISTERED_RESPONSE, LOGIN_UNAUTHORIZED_RESPONSE
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import register, login, token_login, EmailRegistered
from app.services.exceptions import UnauthorizedUser

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
    try:
        return register(user, user_repository)
    except EmailRegistered as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )


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
    try:
        return login(user, user_repository)
    except UnauthorizedUser as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )



@router.post("/token", include_in_schema=False)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repository: UserRepositoryDep
):
    return token_login(form_data, user_repository)
