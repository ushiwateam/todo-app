from sqlalchemy.orm import Session

from app.models import User, Todo
from app.schemas.todo import TodosCreate


def create_todo(todo: TodosCreate, user: User, db: Session):
    todo = Todo(
        title=todo.title,
        description=todo.description,
        user_id=user.id
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo