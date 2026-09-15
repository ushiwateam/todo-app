from app.exceptions import BusinessError


class UnauthorizedAccessError(BusinessError):
    detail = "Access unauthorized"


class TodoNotFoundError(BusinessError):
    detail = "Todo not found"
