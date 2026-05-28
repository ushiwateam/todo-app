from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models import User, Todo
from app.schemas.todo import TodosCreate, AllTodosOut


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


def get_todos(user: User, db: Session, page, limit):
    offset = (page - 1) * limit
    total_todos = db.scalar(select(func.count()).select_from(Todo).where(Todo.user_id == user.id)) or 0
    data = list(db.scalars(select(Todo).where(Todo.user_id == user.id).offset(offset).limit(limit)).all())
    return {
        "data": data,
        "page": page,
        "limit": limit,
        "total": total_todos
    }
