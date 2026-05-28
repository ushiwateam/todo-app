from pydantic import BaseModel, Field


class TodosCreate(BaseModel):
    title: str = Field(title="Title", max_length=255)
    description: str | None = Field(title="Description", default=None)


class TodosOut(BaseModel):
    id: int
    title: str = Field(title="Title", max_length=255)
    description: str | None = Field(title="Description", default=None)


class AllTodosOut(BaseModel):
    data: list[TodosOut]
    page: int
    limit: int
    total: int

