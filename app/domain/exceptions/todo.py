from app.exceptions import DomainError


class UnauthorizedAccessError(DomainError):
    detail = "Access unauthorized"