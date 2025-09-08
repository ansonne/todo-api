import random
from fastapi.testclient import TestClient
from app.main import app  # seu FastAPI app

client = TestClient(app)


def test_register_and_login():
    username = f"testuser{random.randint(1,10000)}"
    password = "testpass"

    # Registra usuário
    response = client.post(
        "/users/register", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == username

    # Login usando JSON
    response = client.post(
        "/users/login", json={"username": username, "password": password}
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    token = data["access_token"]

    # Testa acessar endpoint protegido
    headers = {"Authorization": f"Bearer {token}"}
    protected_response = client.get("/tasks/", headers=headers)
    assert protected_response.status_code == 200
