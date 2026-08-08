from abc import ABC, abstractmethod

from app.business.entities import User
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
    def get_current_user(self, token: str) -> User:
        pass

    @abstractmethod
    def token_login(self, email, password):
        pass
