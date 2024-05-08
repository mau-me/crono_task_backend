from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserResponseSchema]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    tag: str
    state: str


class TodoResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    tag: str
    state: str


class TodoList(BaseModel):
    todos: list[TodoResponseSchema]
