from app.exceptions import BusinessError


class EmailAlreadyRegisteredError(BusinessError):
    detail = "Email already registered"


class InvalidCredentialsError(BusinessError):
    detail = "Email inexistant ou mot de passe incorrect"
