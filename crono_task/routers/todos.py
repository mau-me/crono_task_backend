from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crono_task.database import get_session
from crono_task.models import Todo, User
from crono_task.schemas import TodoResponseSchema, TodoSchema
from crono_task.security import get_current_user

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


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
