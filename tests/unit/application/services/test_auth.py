from unittest.mock import Mock, patch

from pytest import raises

from app.auth.business.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.auth.business.service import AuthService
from app.auth.data_access.model import User

user_id = 1
name = "user"
email = "user@example.com"
password = "password"
hashed_password = "hashed-password"
token = "test-token"


def test_register_user() -> None:
    repository = Mock()
    repository.get_user_by_email.return_value = None

    repository.create.return_value = Mock(
        id=user_id,
        email=email,
    )

    service = AuthService(repository)

    with (
        patch(
            "app.auth.business.service.pwd_context.hash",
            return_value="hashed-password",
        ),
        patch(
            "app.auth.business.service.prepare_token_data",
            return_value={"sub": "1", "email": "user@example.com"},
        ),
        patch(
            "app.auth.business.service.create_access_token",
            return_value="test-token",
        ),
    ):
        result = service.register(name=name, email=email, password=password)

    assert result == {"token": token}
    repository.register_user.assert_called_once()

    created_user = repository.register_user.call_args.args[0]

    assert created_user.email == email
    assert created_user.password == hashed_password


def test_register_email_user() -> None:
    repository = Mock()
    repository.get_user_by_email.return_value = User(
        id=user_id, name=name, email=email, password=hashed_password
    )

    service = AuthService(repository)

    with raises(EmailAlreadyRegisteredError, match="Email already registered"):
        service.register(name=name, email=email, password=password)

    repository.get_user_by_email.assert_called_once_with(email)
    repository.register_user.assert_not_called()


def test_login_user():
    authenticated_user = User(
        id=user_id, name=name, email=email, password=hashed_password
    )

    repository = Mock()

    service = AuthService(repository)

    with (
        patch(
            "app.auth.business.service.pwd_context.hash",
            return_value=hashed_password,
        ),
        patch(
            "app.auth.business.service.prepare_token_data",
            return_value={"sub": str(user_id), "email": email},
        ),
        patch(
            "app.auth.business.service.create_access_token",
            return_value=token,
        ),
        patch.object(
            service,
            "authenticate_user",
            return_value=authenticated_user,
        ) as mock_authenticate,
    ):
        result = service.login(email=email, password=password)

    assert result == {"token": token}
    mock_authenticate.assert_called_once_with(email, password)


def test_login_non_authenticated_user_():
    repository = Mock()

    service = AuthService(repository)

    with (
        patch(
            "app.auth.business.service.pwd_context.hash",
            return_value=hashed_password,
        ),
        patch(
            "app.auth.business.service.prepare_token_data",
            return_value={"sub": str(user_id), "email": email},
        ),
        patch(
            "app.auth.business.service.create_access_token",
            return_value=token,
        ),
        patch.object(
            service,
            "authenticate_user",
            return_value=None,
        ) as mock_authenticate,
    ):
        with raises(
            InvalidCredentialsError, match="Email inexistant ou mot de passe incorrect"
        ):
            service.login(email=email, password=password)
    mock_authenticate.assert_called_once_with(email, password)
