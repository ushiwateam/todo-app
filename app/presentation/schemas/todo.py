from pydantic import BaseModel, Field


class TodosCreateRequest(BaseModel):
    title: str = Field(title="Title", max_length=255)
    description: str | None = Field(title="Description", default=None)


class TodosResponse(BaseModel):
    id: int
    title: str = Field(title="Title", max_length=255)
    description: str | None = Field(title="Description", default=None)


class TodoListResponse(BaseModel):
    data: list[TodosResponse]
    page: int
    limit: int
    total: int

class TodosUpdateRequest(BaseModel):
    title: str = Field(title="Title", max_length=255)
    description: str | None = Field(title="Description", default=None)


class TodosPatchRequest(BaseModel):
    title: str | None = Field(title="Title", max_length=255, default=None)
    description: str | None = Field(title="Description", default=None)
