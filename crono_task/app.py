from http import HTTPStatus

from fastapi import FastAPI

from crono_task.schemas import Message

app = FastAPI()

# AAA - Arrange, Act, Assert


@app.get('/', response_model=Message, status_code=HTTPStatus.OK.value)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/{name}', response_model=Message, status_code=HTTPStatus.OK.value)
def read_name(name: str):
    return {'message': f'Olá {name}!'}
