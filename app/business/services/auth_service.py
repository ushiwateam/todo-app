from datetime import timedelta

from jose import JWTError

from app.business.interfaces.auth import IAuthService
from app.config import ACCESS_TOKEN_EXPIRE_HOURS
from app.business.exceptions.user import InvalidCredentialsError
from app.business.exceptions.user import EmailAlreadyRegisteredError
from app.security import create_access_token, prepare_token_data, pwd_context, decode_access_token
from app.business.entities.user import User

DUMMY_HASH = pwd_context.hash("dummypassword")


class AuthService(IAuthService):

    def register(self, email: str, name: str, password: str):
        existing_user = self.user_repository.get_user_by_email(email)

        if existing_user:
            raise EmailAlreadyRegisteredError()

        hashed_password = pwd_context.hash(password)

        new_entity_user = User(
            name=name,
            email=email,
            password=hashed_password
        )
        new_user = self.user_repository.register_user(new_entity_user)

        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        token_data = prepare_token_data(new_user)
        token = create_access_token(token_data, access_token_expires)
        return {"token": token}

    def authenticate_user(self, email, password):
        existing_user = self.user_repository.get_user_by_email(email)
        if not existing_user:
            pwd_context.verify(password, DUMMY_HASH)
            return None
        if not pwd_context.verify(password, existing_user.password):
            return None
        return existing_user

    def login(self, email: str, password: str):
        existing_user = self.authenticate_user(email, password)
        if not existing_user:
            raise InvalidCredentialsError()
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        token_data = prepare_token_data(existing_user)
        token = create_access_token(token_data, access_token_expires)
        return {"token": token}

    def token_login(self, email: str, password: str):
        token = self.login(email=email, password=password)["token"]
        return {"access_token": token, "token_type": "bearer"}

    def get_current_user(self, token: str) -> User:
        try:
            payload = decode_access_token(token)
            user_id = payload.get("sub")
            if user_id is None:
                raise InvalidCredentialsError()
            user_id = int(user_id)
        except (JWTError, ValueError, TypeError):
            raise InvalidCredentialsError()

        existing_user = self.user_repository.get_user_by_id(user_id)
        if existing_user is None or existing_user.email != payload.get("email"):
            raise InvalidCredentialsError()

        return existing_user
