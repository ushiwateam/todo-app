from app.application.commands.todo import TodoCreateCommand, TodoUpdateCommand, TodoPatchCommand
from app.domain.entities.todo import Todo
from app.infrastructure.database.models import User, Todo as TodoModel
from app.infrastructure.repositories import TodoSqlAlchemyRepository
from app.application.services.exceptions import TodoNotFound, AccessUnauthorized


class TodoService:
    def __init__(self, todo_repository: TodoSqlAlchemyRepository, user: User):
        self.todo_repository = todo_repository
        self.user = user

    def create_todo(self, todo: TodoCreateCommand):
        todo_entity = Todo(
            title=todo.title,
            description=todo.description,
            user_id=self.user.id
        )
        return self.todo_repository.create(todo_entity)

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
            raise TodoNotFound()

        if self.user.id != existing_todo.user_id:
            raise AccessUnauthorized()

        return existing_todo

    def update_todo(self, todo_id: int, todo: TodoUpdateCommand):
        existing_todo = self.get_owned_todo(todo_id)

        update_data = todo.model_dump()

        return self.todo_repository.update(existing_todo.id, update_data)

    def patch_todo(self, todo_id: int, todo: TodoPatchCommand):
        existing_todo = self.get_owned_todo(todo_id)

        update_data = todo.model_dump(exclude_unset=True)

        return self.todo_repository.update(existing_todo.id, update_data)

    def delete_todo(self, todo_id: int):
        existing_todo = self.get_owned_todo(todo_id)
        self.todo_repository.delete(existing_todo.id)
