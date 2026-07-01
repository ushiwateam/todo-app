from sqlalchemy import select

from app.models import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    def create_user(self, name: str, email: str, password: str):
        user = User(
            name=name,
            email=email,
            password=password
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_one_user_or_none(self, email: str):
        return self.db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()


