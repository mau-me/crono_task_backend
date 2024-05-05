from http import HTTPStatus

from crono_task.schemas import UserResponseSchema


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
            'email': user.email,
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
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.json()
    assert 'name' in response.json()
    assert 'email' in response.json()
    assert 'password' not in response.json()


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
        '/users/1',
        json={
            'name': 'mauricio',
            'email': 'mauricio@gmail.com',
            'password': 'newSecret',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN

    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_unauthorized(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
