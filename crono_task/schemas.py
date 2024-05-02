from pydantic import BaseModel, EmailStr


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


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserResponseSchema]
