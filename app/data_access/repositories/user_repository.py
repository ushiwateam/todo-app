from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_access.database.models import User as ModelUser
from app.business.entities.user import User as EntityUser
from app.data_access.repositories.base import ISqlAlchemyRepository
from app.data_access.interfaces.user import IUserRepository
from app.data_access.mappers.user import to_model, to_entity


class UserSqlAlchemyRepository(IUserRepository, ISqlAlchemyRepository[EntityUser, ModelUser]):
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
