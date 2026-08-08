import typing
from datetime import timedelta

from sqlalchemy.orm import Session

from app.business.entities.user import User as BusinessUser
from app.config import ACCESS_TOKEN_EXPIRE_HOURS
from app.dependencies import get_current_user
from app.security import create_access_token, prepare_token_data


def test_get_current_user_should_not_depend_on_raw_db_session():
    hints = typing.get_type_hints(get_current_user, include_extras=True)

    param_types = {
        name: (typing.get_args(hint)[0] if typing.get_args(hint) else hint)
        for name, hint in hints.items()
        if name != "return"
    }

    assert Session not in param_types.values(), (
        f"{get_current_user.__name__} has a parameter typed as {Session.__name__} "
        f"({param_types}). Composition-root dependencies must reach persistence through a "
        "data_access repository interface, not a raw database session — depending on "
        f"{Session.__name__} directly bypasses that abstraction."
    )
