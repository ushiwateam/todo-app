from sqlalchemy.orm import Session

from app.infrastructure.database.models import User
from app.infrastructure.repositories.base import IRepository


class UserRepository(IRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def create_user(self, name: str, email: str, password: str) -> User:
        return self.create(
            name=name,
            email=email,
            password=password,
        )

    def get_user_by_email(self, email: str) -> User | None:
        return self.get_one_or_none(User.email == email)


