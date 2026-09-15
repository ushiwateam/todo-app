from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


UNAUTHORIZED_RESPONSE = {401: {"model": ErrorResponse, "description": "Unauthorized"}}
