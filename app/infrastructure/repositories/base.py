from abc import ABC
from typing import Generic, Type, TypeVar, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.database.session import Base

T = TypeVar("T", bound=Base)


class IRepository(ABC, Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def get_by_id(self, instance_id: int) -> T | None:
        return self.db.get(self.model, instance_id)

    def get_one_or_none(self, *conditions) -> T | None:
        return (
            self.db.execute(
                select(self.model).where(*conditions)
            )
            .scalar_one_or_none()
        )
    def get_all(self, *conditions, offset=0, limit=1000) -> List[T] | []:
        return list(self.db.scalars(select(self.model).where(*conditions).offset(offset).limit(limit)).all())

    def delete(self, instance: T) -> None:
        self.db.delete(instance)
        self.db.commit()

    def update(self, instance: T, data: dict):
        for key, value in data.items():
            setattr(instance, key, value)

        self.db.commit()
        self.db.refresh(instance)

        return instance
