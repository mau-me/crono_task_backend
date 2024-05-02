from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'name': 'mauricio',
                'email': 'mauricio@test.com',
                'id': 1,
            }
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'mauricio',
        'email': 'mauricio@test.com',
        'id': 1,
    }


def test_read_user_not_found(client):
    response = client.get('/users/99')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
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
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/99',
        json={
            'name': 'mauricio',
            'email': 'mauricio@gmail.com',
            'password': 'newSecret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/99')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# def test_delete_user_not_found(client):
#     with pytest.raises(HTTPException) as exc_info:
#         client.delete('/users/99')
#     assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
