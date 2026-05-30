from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas.todo import TodosCreate, TodosOut, AllTodosOut, TodosUpdate, TodosPatch
from app.services.todo_service import create_todo, get_todos, update_todo, delete_todo, patch_todo

router = APIRouter(tags=["Todos"], prefix="/todos")


@router.post(
    "/",
    name="Add new todo",
    status_code=201,
    response_model=TodosOut
)
def create_todo_route(
        todo: TodosCreate,
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
):
    return create_todo(todo, user, db)



@router.get(
    "/",
    name="get all todos",
    status_code=200,
    response_model=AllTodosOut
)
def get_todos_route(
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        page: Annotated[int, Query()] = 1,
        limit: Annotated[int, Query()] = 10

):
    return get_todos(user, db, page, limit)



@router.put(
    "/",
    name="update todo",
    status_code=200,
    response_model=TodosOut
)
def update_todo_route(
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        todo_id: Annotated[int, Query()],
        todo: TodosUpdate
):
    return update_todo(user, db, todo_id, todo)

@router.patch(
    "/",
    name="patch todo",
    status_code=200,
    response_model=TodosPatch
)
def patch_todo_route(
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        todo_id: Annotated[int, Query()],
        todo: TodosPatch
):
    return patch_todo(user, db, todo_id, todo)

@router.delete(
    "/",
    name="delete todo",
    status_code=204,
)
def delete_todo_route(
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        todo_id: Annotated[int, Query()]
):
    return delete_todo(user, db, todo_id)
