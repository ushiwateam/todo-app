from app.schemas.user import UserRegister, UserLogin
from app.services.entities import NewUser, UserCredentials


def to_new_user(data: UserRegister) -> NewUser:
    return NewUser(
        name=data.name,
        email=data.email,
        password=data.password,
    )


def to_user_credentials(data: UserLogin) -> UserCredentials:
    return UserCredentials(
        email=data.email,
        password=data.password,
    )