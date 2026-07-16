import pytest

from app.api.schemas.todo import TodosOut, TodosUpdate


@pytest.mark.parametrize(
    "title,description",
    [
        ("todo 1", "desc 1"),
        ("todo 2", None),
    ],
)
def test_create_todo_authenticated(client, create_user, auth_headers, title, description):
    todo_data = {
        "title": title,
        "description": description,
    }
    user = create_user(password="dummypassword")
    response = client.post("/todos/",
                           headers=auth_headers(user),
                           json=todo_data)
    assert response.status_code == 201
    todo = TodosOut(**response.json())
    assert todo.title == todo_data["title"]
    assert todo.description == todo_data["description"]


def test_create_todo_non_authenticated(client):
    todo_data = {
        "title": "test title",
        "description": "dummy description",
    }
    response = client.post("/todos/", json=todo_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_modify_owned_todo(client, create_user, create_todo, auth_headers):
    user = create_user()
    todo = create_todo(user)
    new_todo = {
        "title": "new title",
        "description": "new desc"
    }
    response = client.put(f"/todos/{todo.id}", headers=auth_headers(user), json=new_todo)

    assert response.status_code == 200
    updated_todo = TodosUpdate(**response.json())
    assert updated_todo.title == new_todo["title"]
    assert updated_todo.description == new_todo["description"]


def test_modify_unowned_todo(client, create_user, create_todo, auth_headers):
    user_1 = create_user(
        name="user1",
        email="user1@example.com",
        password="user1password"
    )
    user_2 = create_user(
        name="user2",
        email="user2@example.com",
        password="user2password"
    )
    todo = create_todo(user_1)
    new_todo = {
        "title": "new title",
        "description": "new desc"
    }
    response = client.put(f"/todos/{todo.id}", headers=auth_headers(user_2), json=new_todo)
    assert response.status_code == 403
    assert response.json()["detail"] == "Access unauthorized"


@pytest.mark.parametrize(
    "page,limit",
    [
        (1, 1),
        (2, 1),
        (1, 10),
        (2, 5)
    ],
)
def test_get_todos_pagination(client, create_user, create_todo, auth_headers, page, limit):
    user = create_user()
    todos = [create_todo(user, title=f"title{i}", description=f"desc{i}") for i in range(10)]
    response = client.get("/todos", params={"page": page, "limit": limit}, headers=auth_headers(user))
    assert response.status_code == 200
    res = response.json()
    assert "data" in res
    assert "page" in res and res["page"] == page
    assert "limit" in res
    assert res["limit"] == limit
    assert len(res["data"]) <= limit
    assert "total" in res and res["total"] == len(todos)

