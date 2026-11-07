from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.auth.business.entity import User
from app.config import settings


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.token_secret_key, algorithm=settings.token_algorithm
    )
    return encoded_jwt


def prepare_token_data(user: User):
    return {"sub": str(user.id), "email": user.email}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token, settings.token_secret_key, algorithms=[settings.token_algorithm]
    )
