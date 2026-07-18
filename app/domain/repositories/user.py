from app.domain.entities.user import User
from app.domain.repositories.base import IRepository


class IUserRepository(IRepository):
    def get_user_by_email(self, email: str) -> User | None:
        pass

