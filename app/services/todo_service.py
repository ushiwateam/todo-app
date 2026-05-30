from sqlalchemy.orm import Session
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.models import User, Todo
from app.schemas.todo import TodosCreate, TodosUpdate


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


def update_todo(user: User, db: Session, todo_id: int, todo: TodosUpdate):
    existing_todo = db.execute(
        select(Todo).where(Todo.id == todo_id)
    ).scalar_one_or_none()

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

    for key, value in update_data.items():
        setattr(existing_todo, key, value)

    db.commit()
    db.refresh(existing_todo)

    return existing_todo

