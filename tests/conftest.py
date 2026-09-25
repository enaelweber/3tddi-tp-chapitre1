import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repository import repository

@pytest.fixture(autouse=True)
def reset_repository():
    repository.reset()
    yield

@pytest.fixture
def client():
    return TestClient(app)