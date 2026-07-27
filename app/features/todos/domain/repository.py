from typing import List

from app.features.todos.domain.entity import Todo
from app.shared.domain.base_repository import IRepository


class ITodoRepository(IRepository):
    def count_todos_by_user_id(self, user_id: int) -> Todo:
        pass

    def get_all_by_user_id(self, user_id: int, offset: int = 0, limit: int = 1000) -> List[Todo]:
        pass
