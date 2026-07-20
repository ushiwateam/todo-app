class AppError(Exception):
    detail = "Application error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.detail
        super().__init__(self.detail)


class DomainError(AppError):
    pass


class ApplicationError(AppError):
    pass


class InfrastructureError(AppError):
    pass