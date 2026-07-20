from app.api.schemas.todo import TodosCreateRequest, TodosUpdateRequest, TodosPatchRequest
from app.application.commands.todo import TodoCreateCommand, TodoUpdateCommand, TodoPatchCommand


def to_todos_create_command(data: TodosCreateRequest) -> TodoCreateCommand:
    return TodoCreateCommand(
        title=data.title,
        description=data.description,
    )


def to_todos_update_command(data: TodosUpdateRequest) -> TodoUpdateCommand:
    return TodoUpdateCommand(
        title=data.title,
        description=data.description,
    )


def to_todos_patch_command(data: TodosPatchRequest) -> TodoPatchCommand:
    return TodoPatchCommand(
        title=data.title,
        description=data.description,
    )
