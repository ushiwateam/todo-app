from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserRegister
from app.config import ACCESS_TOKEN_EXPIRE_HOURS
from app.utils import create_access_token

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def register(user_data: UserRegister, db: Session):
    existing_user = db.execute(
        select(User).where(User.email == user_data.email)
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user_data.password)

    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    token_data = {
        "sub": user.id,
        "email": user.email

    }
    token = create_access_token(token_data, access_token_expires)
    return {"token": token}


def login():
    pass
