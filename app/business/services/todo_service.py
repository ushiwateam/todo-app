from typing import Any

from app.business.entities.todo import Todo
from app.business.exceptions.todo import UnauthorizedAccessError
from app.business.interfaces.todo import ITodoService, _UNSET
from app.business.exceptions.todo import TodoNotFoundError


class TodoService(ITodoService):
    def add_todo(self, title: str, description: str | None = None):
        todo_entity = Todo(
            title=title,
            description=description,
            user_id=self.user.id
        )
        return self.todo_repository.add_todo(todo_entity)

    def get_todos(self, page, limit):
        offset = (page - 1) * limit
        total_todos = self.todo_repository.count_todos_by_user_id(self.user.id)
        data = self.todo_repository.get_all_by_user_id(self.user.id, offset, limit)
        return {
            "data": data,
            "page": page,
            "limit": limit,
            "total": total_todos
        }

    def get_owned_todo(
            self,
            todo_id: int,
    ):
        existing_todo = self.todo_repository.get_by_id(todo_id)

        if not existing_todo:
            raise TodoNotFoundError()

        if self.user.id != existing_todo.user_id:
            raise UnauthorizedAccessError()

        return existing_todo

    def update_todo(self, todo_id: int, title: str, description: str | None):
        existing_todo = self.get_owned_todo(todo_id)

        update_data = {
            "title": title,
            "description": description
        }

        return self.todo_repository.modify_todo(existing_todo.id, update_data)

    def patch_todo(
            self,
            todo_id: int,
            *,
            title: str | None | object = _UNSET,
            description: str | None | object = _UNSET,
    ):
        existing_todo = self.get_owned_todo(todo_id)

        update_data: dict[str, Any] = {}

        if title is not _UNSET:
            update_data["title"] = title

        if description is not _UNSET:
            update_data["description"] = description

        return self.todo_repository.modify_todo(existing_todo.id, update_data)

    def delete_todo(self, todo_id: int):
        existing_todo = self.get_owned_todo(todo_id)
        self.todo_repository.delete_todo(existing_todo.id)
