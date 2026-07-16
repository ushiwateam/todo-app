from app.api.schemas.user import UserRegisterRequest, UserLoginRequest
from app.application.commands.user import UserRegisterCommand, UserLoginCommand


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