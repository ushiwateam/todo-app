from app.business.entities import Todo as EntityTodo
from app.data_access.database.models import Todo as TodoModel


def to_entity(model: TodoModel) -> EntityTodo:
    return EntityTodo(
        id=model.id,
        title=model.title,
        description=model.description,
        user_id=model.user_id,
    )


def to_model(entity: EntityTodo) -> TodoModel:
    return TodoModel(
        id=entity.id,
        title=entity.title,
        description=entity.description,
        user_id=entity.user_id,
    )
