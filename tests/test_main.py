from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Application is running",
        "application": "Python CI/CD Demo",
        "version": "1.0.0"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_add():
    response = client.get("/add/10/20")

    assert response.status_code == 200
    assert response.json() == {
        "operation": "addition",
        "result": 30
    }


def test_multiply():
    response = client.get("/multiply/5/4")

    assert response.status_code == 200
    assert response.json() == {
        "operation": "multiplication",
        "result": 20
    }