from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from app.data_access.database.session import Base

TModel = TypeVar("TModel", bound=Base)
TEntity = TypeVar("TEntity")


class ISqlAlchemyRepository(ABC, Generic[TEntity, TModel]):
    def __init__(self, db: Session, model: Type[TModel]):
        self.db = db
        self.model = model

    @staticmethod
    @abstractmethod
    def to_model(entity: TEntity) -> TModel:
        pass

    @staticmethod
    @abstractmethod
    def to_entity(instance: TModel) -> TEntity:
        pass

    def _create(self, entity: TEntity) -> TEntity:
        instance = self.to_model(entity)

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return self.to_entity(instance)

    def _to_entity_or_none(self, instance: TModel | None) -> TEntity | None:
        return self.to_entity(instance) if instance is not None else None

    def _get_by_id_model(self, instance_id: int) -> TModel | None:
        return self.db.get(self.model, instance_id)

    def _get_one_or_none(self, *conditions) -> TEntity | None:
        statement = select(self.model).where(*conditions)
        instance = self.db.execute(statement).scalar_one_or_none()

        return self._to_entity_or_none(instance)

    def get_all(
            self,
            *conditions,
            offset: int = 0,
            limit: int = 1000,
    ) -> list[TEntity]:
        statement = (
            select(self.model)
            .where(*conditions)
            .offset(offset)
            .limit(limit)
        )

        return [self.to_entity(instance) for instance in self.db.scalars(statement)]

    def _delete(self, instance_id: int):
        statement = delete(self.model).where(
            self.model.id == instance_id
        )

        self.db.execute(statement)
        self.db.commit()

    def _update(self, instance_id, data: dict) -> TEntity:
        statement = (
            update(self.model)
            .where(self.model.id == instance_id)
            .values(**data)
            .returning(self.model)
        )

        instance = self.db.execute(statement).scalar_one()

        entity = self.to_entity(instance)

        self.db.commit()

        return entity
