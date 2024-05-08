from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from crono_task.database import get_session
from crono_task.models import Todo, User
from crono_task.schemas import (
    Message,
    TodoList,
    TodoResponseSchema,
    TodoSchema,
    TodoUpdateSchema,
)
from crono_task.security import get_current_user

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.get('/', response_model=TodoList)
def list_todos(  # noqa
    session: Session,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    tag: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = session.query(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    if tag:
        query = query.filter(Todo.tag == tag)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.post('/', response_model=TodoResponseSchema)
def create_todo(todo: TodoSchema, session: Session, user: CurrentUser):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        tag=todo.tag,
        user_id=user.id,
        finished_at=None,
    )

    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)

    return new_todo


@router.patch('/{todo_id}', response_model=TodoResponseSchema)
def patch_todo(
    todo_id: int, session: Session, user: CurrentUser, todo: TodoUpdateSchema
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for field in todo.dict(exclude_none=True):
        setattr(db_todo, field, getattr(todo, field))

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: Session, user: CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}
