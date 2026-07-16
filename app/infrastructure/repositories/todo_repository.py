from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.infrastructure.database.models import Todo
from app.infrastructure.repositories.base import IRepository


class TodoRepository(IRepository[Todo]):
    def __init__(self, db: Session):
        super().__init__(db, Todo)

    def count_todos_by_user_id(self, user_id: int):
        return self.db.scalar(select(func.count()).select_from(Todo).where(Todo.user_id == user_id)) or 0


    def get_all_by_user_id(self, user_id: int, offset: int=0, limit: int=1000):
        return self.get_all(Todo.user_id == user_id, offset=offset, limit=limit)

