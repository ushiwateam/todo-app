from app.features.auth.domain.entity import User
from app.shared.domain.base_repository import IRepository


class IUserRepository(IRepository):
    def get_user_by_email(self, email: str) -> User | None:
        pass

