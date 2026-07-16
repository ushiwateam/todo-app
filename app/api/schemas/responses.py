from app.api.schemas.errors import ErrorResponse

UNAUTHORIZED_RESPONSE = {
    401: {
        "model": ErrorResponse,
        "description": "Unauthorized"
    }}

EMAIL_ALREADY_REGISTERED_RESPONSE = {
    400: {
        "model": ErrorResponse,
        "description": "Email already registered"
    }
}

LOGIN_UNAUTHORIZED_RESPONSE = {
    401: {
        "model": ErrorResponse,
        "description": "Email inexistant ou mot de passe incorrect",
    }
}

NOT_FOUND_RESPONSE = {
    404: {
        "model": ErrorResponse,
        "description": "Todo not found",
    }
}

FORBIDDEN_RESPONSE = {
    403: {
        "model": ErrorResponse,
        "description": "Access unauthorized",
    }
}
