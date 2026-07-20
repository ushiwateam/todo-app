from app.domain.entities import Todo as DomainTodo
from app.infrastructure.database.models import Todo as TodoModel


def to_entity(model: TodoModel) -> DomainTodo:
    return DomainTodo(
        id=model.id,
        title=model.title,
        description=model.description,
        user_id=model.user_id,
    )


def to_model(entity: DomainTodo) -> TodoModel:
    return TodoModel(
        id=entity.id,
        title=entity.title,
        description=entity.description,
        user_id=entity.user_id,
    )
