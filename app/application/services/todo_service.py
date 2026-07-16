from app.infrastructure.database.models import User
from app.infrastructure.repositories import TodoRepository
from app.api.schemas.todo import TodosCreate, TodosUpdate, TodosPatch
from app.application.services.exceptions import UnfoundTodo, AccessUnauthorized

class TodoService:
    def __init__(self, todo_repository: TodoRepository, user: User):
        self.todo_repository = todo_repository
        self.user = user

    def create_todo(self, todo: TodosCreate):
        return self.todo_repository.create(
            title=todo.title,
            description=todo.description,
            user_id=self.user.id
        )


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
            raise UnfoundTodo()

        if self.user.id != existing_todo.user_id:
            raise AccessUnauthorized()

        return existing_todo


    def update_todo(self, todo_id: int, todo: TodosUpdate):
        existing_todo = self.get_owned_todo(todo_id)

        update_data = todo.model_dump()

        return self.todo_repository.update(existing_todo, update_data)


    def patch_todo(self, todo_id: int, todo: TodosPatch):
        existing_todo = self.get_owned_todo(todo_id)

        update_data = todo.model_dump(exclude_unset=True)

        return self.todo_repository.update(existing_todo, update_data)


    def delete_todo(self, todo_id: int):
        existing_todo = self.get_owned_todo(todo_id)

        self.todo_repository.delete(existing_todo)

        return
