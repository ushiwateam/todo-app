from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from app.dependencies import get_db
from app.responses import EMAIL_ALREADY_REGISTERED_RESPONSE, LOGIN_UNAUTHORIZED_RESPONSE
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import register, login, token_login

router = APIRouter(tags=["Users"])


@router.post(
    "/register",
    name="Register a new user",
    responses={
        **EMAIL_ALREADY_REGISTERED_RESPONSE
    }
)
def register_route(
        user: UserRegister,
        db: Annotated[Session, Depends(get_db)]
):
    return register(user, db)


@router.post("/login",
             name="Login an existent user",
             responses={
                 **LOGIN_UNAUTHORIZED_RESPONSE
             }
             )
def login_route(
        user: UserLogin,
        db: Annotated[Session, Depends(get_db)]
):
    return login(user, db)


@router.post("/token", include_in_schema=False)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_db)]
):
    return token_login(form_data, db)
