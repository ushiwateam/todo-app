from unittest.mock import Mock, patch

import pytest

from app.business.entities import Todo
from app.business.services.todo_service import TodoService


@pytest.mark.parametrize(
    "title,description",
    [
        ("todo 1", "desc 1"),
        ("todo 2", None),
    ],
)
def test_add_todo(title, description, create_user_entity):
    user = create_user_entity()
    saved_todo = Todo(
        title=title,
        description=description,
        user_id=user.id
    )
    repository = Mock()
    repository.add_todo.return_value = saved_todo

    service = TodoService(repository, user)

    result = service.add_todo(
        title=saved_todo.title,
        description=saved_todo.description
    )

    repository.add_todo.assert_called_once()

    added_todo = repository.add_todo.call_args.args[0]

    assert added_todo.title == title
    assert added_todo.description == description
    assert added_todo.user_id == user.id
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

    modify_data = {
        "title": "modified_title",
        "description": "modified_description"
    }

    modified_todo = Todo(
        id=existing_todo.id,
        title=modify_data["title"],
        description=modify_data["description"],
        user_id=user.id,
    )
    repository.modify_todo.return_value = modified_todo

    with patch.object(
            service,
            "get_owned_todo",
            return_value=existing_todo,
    ) as mock_owned_todo:
        result = service.update_todo(existing_todo.id,
                                     title=modify_data["title"],
                                     description=modify_data["description"])

    mock_owned_todo.assert_called_once_with(existing_todo.id)
    repository.modify_todo.assert_called_once()

    todo_id, update_data = repository.modify_todo.call_args.args

    assert todo_id == existing_todo.id
    assert update_data.get("title") == modify_data["title"]
    assert update_data.get("description") == modify_data["description"]
    assert result is modified_todo


@pytest.mark.parametrize(
    "title,description,modify_data",
    [
        ("todo 1", "desc 1", {"title": "new_title"}),
        ("todo 1", None, {"description": "new_descr"})
    ],
)
def test_patch_todo(title, description, modify_data, create_user_entity):
    user = create_user_entity()

    existing_todo = Todo(
        id=1,
        title=title,
        description=description,
        user_id=user.id,
    )
    existing_todo_data = existing_todo.model_dump()

    repository = Mock()
    service = TodoService(repository, user)

    modified_todo = Todo(**{**existing_todo_data, **modify_data})
    repository.modify_todo.return_value = modified_todo

    with patch.object(
            service,
            "get_owned_todo",
            return_value=existing_todo,
    ) as mock_owned_todo:
        result = service.patch_todo(existing_todo.id, **modify_data)

    mock_owned_todo.assert_called_once_with(existing_todo.id)
    repository.modify_todo.assert_called_once()

    todo_id, modify_data = repository.modify_todo.call_args.args

    assert todo_id == existing_todo.id
    if "title" in modify_data:
        assert modify_data.get("title") == modify_data["title"]
    if "description" in modify_data:
        assert modify_data.get("description") == modify_data["description"]
    assert result is modified_todo
