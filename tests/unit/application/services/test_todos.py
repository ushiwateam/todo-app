from unittest.mock import Mock, patch

import pytest

from app.domain.entities import Todo
from app.application.commands.todo import TodoCreateCommand, TodoUpdateCommand, TodoPatchCommand
from app.application.services.todo_service import TodoService


@pytest.mark.parametrize(
    "title,description",
    [
        ("todo 1", "desc 1"),
        ("todo 2", None),
    ],
)
def test_create_todo(title, description, create_user_entity):
    user = create_user_entity()
    saved_todo = Todo(
        title=title,
        description=description,
        user_id=user.id
    )
    repository = Mock()
    repository.create.return_value = saved_todo

    service = TodoService(repository, user)

    command = TodoCreateCommand(
        title=saved_todo.title,
        description=saved_todo.description
    )

    result = service.create_todo(command)

    repository.create.assert_called_once()

    created_todo = repository.create.call_args.args[0]

    assert created_todo.title == title
    assert created_todo.description == description
    assert created_todo.user_id == user.id
    assert result is saved_todo


@pytest.mark.parametrize(
    "title,description",
    [
        ("todo 1", "desc 1"),
        ("todo 2", None),
    ],
)
def test_update_todo(title, description, create_user_entity):
    user = create_user_entity()

    existing_todo = Todo(
        id=1,
        title=title,
        description=description,
        user_id=user.id,
    )

    repository = Mock()
    service = TodoService(repository, user)

    command = TodoUpdateCommand(
        title="modified_title",
        description="modified_description",
    )

    modified_todo = Todo(
        id=existing_todo.id,
        title=command.title,
        description=command.description,
        user_id=user.id,
    )
    repository.update.return_value = modified_todo

    with patch.object(
            service,
            "get_owned_todo",
            return_value=existing_todo,
    ) as mock_owned_todo:
        result = service.update_todo(existing_todo.id, command)

    mock_owned_todo.assert_called_once_with(existing_todo.id)
    repository.update.assert_called_once()

    todo_id, update_data = repository.update.call_args.args

    assert todo_id == existing_todo.id
    assert update_data.get("title") == command.title
    assert update_data.get("description") == command.description
    assert result is modified_todo


@pytest.mark.parametrize(
    "title,description,update_data",
    [
        ("todo 1", "desc 1", {"title": "new_title"}),
        ("todo 1", None, {"description": "new_descr"})
    ],
)
def test_patch_todo(title, description, update_data ,create_user_entity):
    user = create_user_entity()

    existing_todo = Todo(
        id=1,
        title=title,
        description=description,
        user_id=user.id,
    )

    repository = Mock()
    service = TodoService(repository, user)

    command = TodoPatchCommand(
        title=update_data.get("title"),
        description=update_data.get("description")
    )

    modified_todo = Todo(
        id=existing_todo.id,
        title=command.title,
        description=command.description,
        user_id=user.id,
    )
    repository.update.return_value = modified_todo

    with patch.object(
            service,
            "get_owned_todo",
            return_value=existing_todo,
    ) as mock_owned_todo:
        result = service.patch_todo(existing_todo.id, command)

    mock_owned_todo.assert_called_once_with(existing_todo.id)
    repository.update.assert_called_once()

    todo_id, update_data = repository.update.call_args.args

    assert todo_id == existing_todo.id
    assert update_data.get("title") == command.title
    assert update_data.get("description") == command.description
    assert result is modified_todo
