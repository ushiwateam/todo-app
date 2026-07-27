from sqlalchemy.orm import Session

from app.features.auth.infrastrcuture.model import User as ModelUser
from app.features.auth.domain.entity import User as DomainUser
from app.shared.infrastructure.base_repository import ISqlAlchemyRepository
from app.features.auth.domain.repository import IUserRepository
from app.features.auth.infrastrcuture.mapper import to_model, to_entity


class UserSqlAlchemyRepository(ISqlAlchemyRepository[DomainUser, ModelUser], IUserRepository):
    def __init__(self, db: Session):
        super().__init__(db, ModelUser)

    @staticmethod
    def to_model(entity: DomainUser) -> ModelUser:
        return to_model(entity)

    @staticmethod
    def to_entity(instance: ModelUser) -> DomainUser:
        return to_entity(instance)

    def get_user_by_email(self, email: str) -> DomainUser | None:
        instance = self.get_one_or_none(ModelUser.email == email)
        return self._to_entity_or_none(instance)


