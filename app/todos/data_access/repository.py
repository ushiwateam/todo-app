from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.shared.database.repository import ISqlAlchemyRepository
from app.todos.business.entity import Todo
from app.todos.business.entity import Todo as EntityTodo
from app.todos.data_access.interface import ITodoRepository
from app.todos.data_access.mapper import to_entity, to_model
from app.todos.data_access.model import Todo as ModelTodo


class TodoSqlAlchemyRepository(
    ISqlAlchemyRepository[EntityTodo, ModelTodo], ITodoRepository
):

    def __init__(self, db: Session):
        super().__init__(db, ModelTodo)

    @staticmethod
    def to_model(entity: EntityTodo) -> ModelTodo:
        return to_model(entity)

    @staticmethod
    def to_entity(instance: ModelTodo) -> EntityTodo:
        return to_entity(instance)

    def get_by_id(self, todo_id: int) -> EntityTodo | None:
        return self._to_entity_or_none(self._get_by_id_model(todo_id))

    def count_todos_by_user_id(self, user_id: int):
        return (
            self.db.scalar(
                select(func.count())
                .select_from(ModelTodo)
                .where(ModelTodo.user_id == user_id)
            )
            or 0
        )

    def get_all_by_user_id(
        self, user_id: int, offset: int = 0, limit: int = 1000
    ) -> List[EntityTodo]:
        return self.get_all(ModelTodo.user_id == user_id, offset=offset, limit=limit)

    def add_todo(self, todo: Todo):
        return self._create(todo)

    def modify_todo(self, todo_id: int, update_data: dict):
        return self._update(todo_id, update_data)

    def delete_todo(self, todo_id: int):
        return self._delete(todo_id)
