from typing import Annotated

from fastapi import APIRouter, Query, Path, HTTPException, status

from app.api.mappers.todo import to_todos_create_command, to_todos_update_command, to_todos_patch_command
from app.dependencies import TodoServiceDep
from app.api.responses import UNAUTHORIZED_RESPONSE, FORBIDDEN_RESPONSE, NOT_FOUND_RESPONSE
from app.api.schemas.todo import TodosCreateRequest, TodosResponse, TodoListResponse, TodosUpdateRequest, TodosPatchRequest
from app.application.services.exceptions import TodoNotFound, AccessUnauthorized

router = APIRouter(tags=["Todos"], prefix="/todos", responses={
    **UNAUTHORIZED_RESPONSE
}
                   )


@router.post(
    "/",
    name="Add new todo",
    status_code=201,
    response_model=TodosResponse,
)
def create_todo_route(
        todo: TodosCreateRequest,
        todo_service: TodoServiceDep
):
    return todo_service.create_todo(to_todos_create_command(todo))


@router.get(
    "/",
    name="get all todos",
    status_code=200,
    response_model=TodoListResponse
)
def get_todos_route(
        todo_service: TodoServiceDep,
        page: Annotated[int, Query()] = 1,
        limit: Annotated[int, Query()] = 10

):
    return todo_service.get_todos(page, limit)


@router.put(
    "/{todo_id}",
    name="update todo",
    status_code=200,
    response_model=TodosResponse,
    responses={
        **FORBIDDEN_RESPONSE,
        **NOT_FOUND_RESPONSE
    }
)
def update_todo_route(
        todo_service: TodoServiceDep,
        todo_id: Annotated[int, Path()],
        todo: TodosUpdateRequest
):
    try:
        return todo_service.update_todo(todo_id, to_todos_update_command(todo))
    except TodoNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except AccessUnauthorized as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail
        )


@router.patch(
    "/{todo_id}",
    name="patch todo",
    status_code=200,
    response_model=TodosPatchRequest,
    responses={
        **FORBIDDEN_RESPONSE,
        **NOT_FOUND_RESPONSE
    }
)
def patch_todo_route(
        todo_service: TodoServiceDep,
        todo_id: Annotated[int, Path()],
        todo: TodosPatchRequest
):
    try:
        return todo_service.patch_todo(todo_id, to_todos_patch_command(todo))
    except TodoNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except AccessUnauthorized as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail
        )


@router.delete(
    "/{todo_id}",
    name="delete todo",
    status_code=204,
    responses={
        **FORBIDDEN_RESPONSE,
        **NOT_FOUND_RESPONSE
    }
)
def delete_todo_route(
        todo_service: TodoServiceDep,
        todo_id: Annotated[int, Path()]
):
    try:
        return todo_service.delete_todo(todo_id)
    except TodoNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except AccessUnauthorized as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail
        )
