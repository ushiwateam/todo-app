from fastapi import APIRouter, status, HTTPException

from app.api.dependencies import AuthServiceDep, FormDataDep
from app.api.responses import EMAIL_ALREADY_REGISTERED_RESPONSE, LOGIN_UNAUTHORIZED_RESPONSE
from app.api.mappers import to_new_user, to_user_credentials
from app.api.schemas.user import UserRegister, UserLogin
from app.application.services.auth_service import EmailRegistered
from app.application.services.exceptions import UnauthorizedUser

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
        user: UserRegister,
        auth_service: AuthServiceDep
):
    try:
        return auth_service.register(to_new_user(user))
    except EmailRegistered as e:
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
        user: UserLogin,
        auth_service: AuthServiceDep
):
    try:
        return auth_service.login(to_user_credentials(user))
    except UnauthorizedUser as e:
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
