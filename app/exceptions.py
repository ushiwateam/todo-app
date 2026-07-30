class AppError(Exception):
    detail = "Application error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.detail
        super().__init__(self.detail)


class PresentationError(AppError):
    pass


class DataAccessError(AppError):
    pass


class BusinessError(AppError):
    pass
