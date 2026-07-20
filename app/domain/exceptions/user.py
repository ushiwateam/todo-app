from app.exceptions import DomainError


class EmailAlreadyRegisteredError(DomainError):
    detail = "Email already registered"
