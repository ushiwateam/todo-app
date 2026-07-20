from typing import List

from app.domain.repositories.base import IRepository
from app.domain.entities.todo import Todo


class ITodoRepository(IRepository):
    def count_todos_by_user_id(self, user_id: int) -> Todo:
        pass

    def get_all_by_user_id(self, user_id: int, offset: int = 0, limit: int = 1000) -> List[Todo]:
        pass