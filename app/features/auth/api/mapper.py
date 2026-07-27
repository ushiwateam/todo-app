from app.features.auth.api.schemas import UserRegisterRequest, UserLoginRequest
from app.features.auth.application.commands import UserRegisterCommand, UserLoginCommand


def to_user_register_command(data: UserRegisterRequest) -> UserRegisterCommand:
    return UserRegisterCommand(
        name=data.name,
        email=data.email,
        password=data.password,
    )


def to_user_login_command(data: UserLoginRequest) -> UserLoginCommand:
    return UserLoginCommand(
        email=data.email,
        password=data.password,
    )