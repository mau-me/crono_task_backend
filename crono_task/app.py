from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from crono_task.routers import auth, todos, users
from crono_task.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)

app.include_router(users.router)
# AAA - Arrange, Act, Assert


@app.get('/')
async def docs_redirect():
    return RedirectResponse(url='/docs')
