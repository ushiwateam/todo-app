from abc import ABC, abstractmethod

from fastapi.security import OAuth2PasswordRequestForm

from app.data_access.interfaces.user import IUserRepository


class IAuthService(ABC):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    @abstractmethod
    def register(self, email: str, name: str, password: str):
        pass

    @abstractmethod
    def login(self, email: str, password: str):
        pass

    @abstractmethod
    def token_login(self, form_data: OAuth2PasswordRequestForm):
        pass
