from http import HTTPStatus

from fastapi import FastAPI

from crono_task.routers import auth, users
from crono_task.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

app.include_router(users.router)
# AAA - Arrange, Act, Assert


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}
