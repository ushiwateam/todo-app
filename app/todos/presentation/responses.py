from app.shared.errors.responses import ErrorResponse

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
