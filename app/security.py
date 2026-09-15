from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.auth.data_access.model import User
from app.config import TOKEN_ALGORITHM, TOKEN_SECRET_KEY


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt


def prepare_token_data(user: User):
    return {"sub": str(user.id), "email": user.email}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
