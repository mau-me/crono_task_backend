from http import HTTPStatus

from fastapi.testclient import TestClient

from crono_task.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_name_deve_retornar_ok_e_ola_nome():
    client = TestClient(app)

    nome = 'mauricio'

    response = client.get(f'/{nome}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': f'Olá {nome}!'}
