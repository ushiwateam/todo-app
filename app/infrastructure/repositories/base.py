from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from app.infrastructure.database.session import Base

TModel = TypeVar("TModel", bound=Base)
TDomain = TypeVar("TDomain")


class ISqlAlchemyRepository(ABC, Generic[TDomain, TModel]):
    def __init__(self, db: Session, model: Type[TModel]):
        self.db = db
        self.model = model

    @staticmethod
    @abstractmethod
    def to_model(entity: TDomain) -> TModel:
        pass

    @staticmethod
    @abstractmethod
    def to_entity(instance: TModel) -> TDomain:
        pass

    def create(self, entity: TDomain) -> TDomain:
        instance = self.to_model(entity)

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return self.to_entity(instance)

    def _to_entity_or_none(self, instance: TModel | None) -> TDomain | None:
        return self.to_entity(instance) if instance is not None else None

    def get_by_id(self, instance_id: int) -> TDomain | None:
        return self._to_entity_or_none(self._get_by_id_model(instance_id))

    def _get_by_id_model(self, instance_id: int) -> TModel | None:
        return self.db.get(self.model, instance_id)

    def get_one_or_none(self, *conditions) -> TDomain | None:
        statement = select(self.model).where(*conditions)
        instance = self.db.execute(statement).scalar_one_or_none()

        return self._to_entity_or_none(instance)

    def get_all(
            self,
            *conditions,
            offset: int = 0,
            limit: int = 1000,
    ) -> list[TDomain]:
        statement = (
            select(self.model)
            .where(*conditions)
            .offset(offset)
            .limit(limit)
        )

        return [self.to_entity(instance) for instance in self.db.scalars(statement)]

    def delete(self, instance_id: int):
        statement = delete(self.model).where(
            self.model.id == instance_id
        )

        self.db.execute(statement)
        self.db.commit()

    def update(self, instance_id, data: dict) -> TDomain:
        statement = (
            update(self.model)
            .where(self.model.id == instance_id)
            .values(**data)
            .returning(self.model)
        )

        instance = self.db.execute(statement).scalar_one()

        domain_entity = self.to_entity(instance)

        self.db.commit()

        return domain_entity
