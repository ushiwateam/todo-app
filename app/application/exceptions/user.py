from app.exceptions import ApplicationError


class InvalidCredentialsError(ApplicationError):
    detail = "Email inexistant ou mot de passe incorrect"