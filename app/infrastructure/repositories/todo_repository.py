from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.domain.repositories.todo import ITodoRepository
from app.infrastructure.database.models import Todo as ModelTodo
from app.infrastructure.mappers.todo import to_model, to_entity
from app.infrastructure.repositories.base import ISqlAlchemyRepository
from app.domain.entities.todo import Todo as DomainTodo


class TodoSqlAlchemyRepository(ISqlAlchemyRepository[DomainTodo, ModelTodo], ITodoRepository):
    def __init__(self, db: Session):
        super().__init__(db, ModelTodo)

    @staticmethod
    def to_model(entity: DomainTodo) -> ModelTodo:
        return to_model(entity)

    @staticmethod
    def to_entity(instance: ModelTodo) -> DomainTodo:
        return to_entity(instance)

    def count_todos_by_user_id(self, user_id: int):
        return self.db.scalar(select(func.count()).select_from(ModelTodo).where(ModelTodo.user_id == user_id)) or 0


    def get_all_by_user_id(self, user_id: int, offset: int=0, limit: int=1000) -> List[DomainTodo]:
        return self.get_all(ModelTodo.user_id == user_id, offset=offset, limit=limit)

