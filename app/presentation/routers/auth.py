from fastapi import APIRouter, status, HTTPException

from app.business.exceptions.user import InvalidCredentialsError
from app.dependencies import AuthServiceDep, FormDataDep
from app.presentation.error_responses import EMAIL_ALREADY_REGISTERED_RESPONSE, LOGIN_UNAUTHORIZED_RESPONSE

from app.presentation.schemas.user import UserRegisterRequest, UserLoginRequest
from app.business.exceptions.user import EmailAlreadyRegisteredError
from tests.unit.application.services.test_auth import password

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
        return auth_service.register(
            email=user.email,
            name=user.name,
            password=user.password)
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
        return auth_service.login(
            email=user.email,
            password=user.password
        )
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
    return auth_service.token_login(email=form_data.username, password=form_data.password)
