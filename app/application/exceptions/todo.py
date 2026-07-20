from app.exceptions import ApplicationError


class TodoNotFoundError(ApplicationError):
    detail = "Todo not found"
