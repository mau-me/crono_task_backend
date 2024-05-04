from http import HTTPStatus

from crono_task.schemas import UserResponseSchema


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'name': 'mauricio',
            'email': 'mauricio@test.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'mauricio',
        'email': 'mauricio@test.com',
        'id': 1,
    }


def test_create_user_already_exists(client, user):
    response = client.post(
        '/users',
        json={
            'name': 'Teste',
            'email': 'test@test.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User with this email already exists'}


def test_read_users(client, user):
    user_schema = UserResponseSchema.model_validate(user).model_dump()
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get('/users/1')

    # assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'Teste',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_user_not_found(client):
    response = client.get('/users/99')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'mauricio',
            'email': 'mauricio@gmail.com',
            'password': 'newSecret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'mauricio',
        'email': 'mauricio@gmail.com',
        'id': user.id,
    }


def test_update_user_unauthorized(client):
    response = client.put(
        '/users/99',
        json={
            'name': 'mauricio',
            'email': 'mauricio@gmail.com',
            'password': 'newSecret',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_unauthorized(client):
    response = client.delete('/users/99')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
