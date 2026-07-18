from app.domain.entities import User as DomainUser
from app.infrastructure.database.models import User as UserModel


def to_entity(model: UserModel) -> DomainUser:
    return DomainUser(
        id=model.id,
        name=model.name,
        email=model.email,
        password=model.password,
    )


def to_model(entity: DomainUser) -> UserModel:
    return UserModel(
        id=entity.id,
        name=entity.name,
        email=entity.email,
        password=entity.password,
    )