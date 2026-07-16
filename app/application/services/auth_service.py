from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm

from app.infrastructure.repositories import UserRepository
from app.application.commands.user import UserRegisterCommand, UserLoginCommand
from app.config import ACCESS_TOKEN_EXPIRE_HOURS
from app.application.services.exceptions import EmailRegistered, UnauthorizedUser
from app.application.services.utils import create_access_token, prepare_token_data, pwd_context

DUMMY_HASH = pwd_context.hash("dummypassword")


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, user: UserRegisterCommand):
        existing_user = self.user_repository.get_user_by_email(user.email)

        if existing_user:
            raise EmailRegistered()

        hashed_password = pwd_context.hash(user.password)

        new_user = self.user_repository.create_user(
            name=user.name,
            email=user.email,
            password=hashed_password
        )

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

    def login(self, user: UserLoginCommand):
        existing_user = self.authenticate_user(user.email, user.password)
        if not existing_user:
            raise UnauthorizedUser()
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        token_data = prepare_token_data(existing_user)
        token = create_access_token(token_data, access_token_expires)
        return {"token": token}

    def token_login(self, form_data: OAuth2PasswordRequestForm):
        existing_user = self.authenticate_user(form_data.username, form_data.password)
        if not existing_user:
            raise UnauthorizedUser()
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        token_data = prepare_token_data(existing_user)
        token = create_access_token(token_data, access_token_expires)
        return {"access_token": token, "token_type": "bearer"}
