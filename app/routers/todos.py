from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas.todo import TodosCreate, TodosOut
from app.services.todo_service import create_todo

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
