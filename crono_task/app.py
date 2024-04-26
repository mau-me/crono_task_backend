from fastapi import FastAPI

app = FastAPI()

# AAA - Arrange, Act, Assert


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/{name}')
def read_name(name: str):
    return {'message': f'Olá {name}!'}
