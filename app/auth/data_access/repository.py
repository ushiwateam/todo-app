from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.business.entity import User as EntityUser
from app.auth.data_access.interface import IUserRepository
from app.auth.data_access.mapper import to_entity, to_model
from app.auth.data_access.model import User as ModelUser
from app.shared.database.repository import ISqlAlchemyRepository


class UserSqlAlchemyRepository(
    IUserRepository, ISqlAlchemyRepository[EntityUser, ModelUser]
):
    def __init__(self, db: Session):
        super().__init__(db, ModelUser)

    @staticmethod
    def to_model(entity: EntityUser) -> ModelUser:
        return to_model(entity)

    @staticmethod
    def to_entity(instance: ModelUser) -> EntityUser:
        return to_entity(instance)

    def register_user(self, user: EntityUser):
        return self._create(user)

    def get_user_by_email(self, email: str) -> EntityUser | None:
        instance = self._get_one_or_none(ModelUser.email == email)
        return self._to_entity_or_none(instance)

    def get_user_by_id(self, user_id: int) -> EntityUser | None:
        return self._to_entity_or_none(self._get_by_id_model(instance_id=user_id))
