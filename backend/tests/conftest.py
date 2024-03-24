import pytest
from fastapi.testclient import TestClient

from my_app_api.routes import app


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
