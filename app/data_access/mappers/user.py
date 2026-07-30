from app.business.entities import User as EntityUser
from app.data_access.database.models import User as UserModel


def to_entity(model: UserModel) -> EntityUser:
    return EntityUser(
        id=model.id,
        name=model.name,
        email=model.email,
        password=model.password,
    )


def to_model(entity: EntityUser) -> UserModel:
    return UserModel(
        id=entity.id,
        name=entity.name,
        email=entity.email,
        password=entity.password,
    )