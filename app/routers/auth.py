from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.dependencies import get_db
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import register, login

router = APIRouter(tags=["Users"])


@router.post(
    "/register",
    name="Register a new user"
)
def register_route(
    user: UserRegister,
    db: Annotated[Session, Depends(get_db)]
):
    return register(user, db)

@router.post("/login",
             name="Login an existent user")
def login_route(
    user: UserLogin,
    db: Annotated[Session, Depends(get_db)]
):
    return login(user, db)
