from fastapi import APIRouter, status, HTTPException

from app.application.exceptions import InvalidCredentialsError
from app.dependencies import AuthServiceDep, FormDataDep
from app.api.responses import EMAIL_ALREADY_REGISTERED_RESPONSE, LOGIN_UNAUTHORIZED_RESPONSE
from app.api.mappers import to_user_register_command, to_user_login_command
from app.api.schemas.user import UserRegisterRequest, UserLoginRequest
from app.domain.exceptions import EmailAlreadyRegisteredError

router = APIRouter(tags=["Users"])


@router.post(
    "/register",
    name="Register a new user",
    status_code=status.HTTP_201_CREATED,
    responses={
        **EMAIL_ALREADY_REGISTERED_RESPONSE
    }
)
def register_route(
        user: UserRegisterRequest,
        auth_service: AuthServiceDep
):
    try:
        return auth_service.register(to_user_register_command(user))
    except EmailAlreadyRegisteredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )


@router.post("/login",
             name="Login an existent user",
             responses={
                 **LOGIN_UNAUTHORIZED_RESPONSE
             }
             )
def login_route(
        user: UserLoginRequest,
        auth_service: AuthServiceDep
):
    try:
        return auth_service.login(to_user_login_command(user))
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )


@router.post("/token", include_in_schema=False)
async def login_for_access_token(
        auth_service: AuthServiceDep,
        form_data: FormDataDep
):
    return auth_service.token_login(form_data)
