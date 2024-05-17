from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from crono_task.routers import auth, todos, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],

)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)

app.include_router(users.router)
# AAA - Arrange, Act, Assert


@app.get('/')
async def docs_redirect():
    return RedirectResponse(url='/docs')
