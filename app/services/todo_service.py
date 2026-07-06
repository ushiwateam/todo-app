from fastapi import HTTPException, status

from app.dependencies import TodoRepositoryDep
from app.models import User
from app.schemas.todo import TodosCreate, TodosUpdate, TodosPatch


def create_todo(todo: TodosCreate, user: User, todo_repository: TodoRepositoryDep):
    return todo_repository.create(
        title=todo.title,
        description=todo.description,
        user_id=user.id
    )


def get_todos(user: User, todo_repository: TodoRepositoryDep, page, limit):
    offset = (page - 1) * limit
    total_todos = todo_repository.count_todos_by_user_id(user.id)
    data = todo_repository.get_all_by_user_id(user.id, offset, limit)
    return {
        "data": data,
        "page": page,
        "limit": limit,
        "total": total_todos
    }


def update_todo(user: User, todo_repository: TodoRepositoryDep, todo_id: int, todo: TodosUpdate):
    existing_todo = todo_repository.get_by_id(todo_id)

    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    if user.id != existing_todo.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access unauthorized"
        )

    update_data = todo.model_dump()

    return todo_repository.update(existing_todo, update_data)


def patch_todo(user: User, todo_repository: TodoRepositoryDep, todo_id: int, todo: TodosPatch):
    existing_todo = todo_repository.get_by_id(todo_id)

    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    if user.id != existing_todo.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access unauthorized"
        )

    update_data = todo.model_dump(exclude_unset=True)

    return todo_repository.update(existing_todo, update_data)


def delete_todo(user: User, todo_repository: TodoRepositoryDep, todo_id: int):
    existing_todo = todo_repository.get_by_id(todo_id)

    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    if user.id != existing_todo.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access unauthorized"
        )

    todo_repository.delete(existing_todo)

    return
