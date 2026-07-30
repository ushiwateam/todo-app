from abc import ABC, abstractmethod

from app.business.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def register_user(self, user: User):
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        pass
