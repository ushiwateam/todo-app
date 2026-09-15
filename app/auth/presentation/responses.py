from app.shared.errors.responses import ErrorResponse

EMAIL_ALREADY_REGISTERED_RESPONSE = {
    400: {"model": ErrorResponse, "description": "Email already registered"}
}

LOGIN_UNAUTHORIZED_RESPONSE = {
    401: {
        "model": ErrorResponse,
        "description": "Email inexistant ou mot de passe incorrect",
    }
}
