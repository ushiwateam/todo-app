from typing import List
from abc import ABC, abstractmethod

from app.business.entities.todo import Todo


class ITodoRepository(ABC):

    @abstractmethod
    def add_todo(self, todo: Todo):
       pass

    @abstractmethod
    def count_todos_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    def get_all_by_user_id(self, user_id: int, offset: int = 0, limit: int = 1000) -> List[Todo]:
        pass

    @abstractmethod
    def get_by_id(self, todo_id: int):
        pass

    @abstractmethod
    def modify_todo(self, todo_id: int, update_data: dict):
        pass

    @abstractmethod
    def delete_todo(self, todo_id: int):
        pass