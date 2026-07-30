from abc import ABC, abstractmethod
from typing import Any

from app.business.entities.user import User
from app.data_access.interfaces.todo import ITodoRepository

_UNSET = object()


class ITodoService(ABC):
    def __init__(self, todo_repository: ITodoRepository, user: User):
        self.todo_repository = todo_repository
        self.user = user

    @abstractmethod
    def add_todo(self, title: str, description: str | None = None):
        pass

    @abstractmethod
    def get_todos(self, page, limit):
        pass

    @abstractmethod
    def get_owned_todo(self, todo_id: int, ):
        pass

    @abstractmethod
    def update_todo(self, todo_id: int, title: str, description: str | None):
        pass

    @abstractmethod
    def patch_todo(
            self,
            todo_id: int,
            *,
            title: str | None | object = _UNSET,
            description: str | None | object = _UNSET
    ):
        pass


    @abstractmethod
    def delete_todo(self, todo_id: int):
        pass
