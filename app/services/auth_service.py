from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserRegister


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def register(
    user_data: UserRegister,
    db: Session
) -> User:

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

    return {"message": f"User {user.name} created successfully"}