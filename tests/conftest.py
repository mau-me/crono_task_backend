import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from crono_task.app import app
from crono_task.database import get_session
from crono_task.models import table_registry
from crono_task.security import get_password_hash
from tests.factories import UserFactory


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    yield session

    session.close()
    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    password = 'test'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'test'

    return user


@pytest.fixture()
def other_user(session):
    password = 'test'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'test'

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    return response.json()['access_token']
