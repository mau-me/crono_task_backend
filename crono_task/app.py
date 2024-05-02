from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from crono_task.schemas import (
    Message,
    UserDB,
    UserList,
    UserResponseSchema,
    UserSchema,
)

app = FastAPI()

database = []

# AAA - Arrange, Act, Assert


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post(
    '/users', response_model=UserResponseSchema, status_code=HTTPStatus.CREATED
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=UserResponseSchema)
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_index = user_id - 1

    user = database[user_index]

    return user


@app.put(
    '/users/{user_id}',
    response_model=UserResponseSchema,
    status_code=HTTPStatus.OK,
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_index = user_id - 1

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_index] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_index = user_id - 1
    del database[user_index]

    return {'message': 'User deleted'}
