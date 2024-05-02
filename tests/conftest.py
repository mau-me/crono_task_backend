import pytest
from fastapi.testclient import TestClient

from crono_task.app import app


@pytest.fixture()
def client():
    return TestClient(app)
