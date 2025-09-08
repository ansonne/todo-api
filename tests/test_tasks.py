from fastapi.testclient import TestClient
from app import main, database, models

client = TestClient(main.app)


def get_token():
    username = "taskuser"
    password = "taskpass"
    client.post("/users/register", json={"username": username, "password": password})
    response = client.post(
        "/users/login", json={"username": username, "password": password}
    )
    return response.json()["access_token"]


def test_task_crud():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Criar
    response = client.post("/tasks/", json={"title": "Test Task"}, headers=headers)
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Listar
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    assert any(t["id"] == task_id for t in response.json())

    # Atualizar
    response = client.put(
        f"/tasks/{task_id}", json={"completed": True}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_task_stats():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Limpa tasks do usuário antes de criar novas
    db = next(database.get_db())
    db.query(models.Task).filter(models.Task.owner_id == 1).delete()
    db.commit()

    client.post("/tasks/", json={"title": "Task 1"}, headers=headers)
    client.post("/tasks/", json={"title": "Task 2", "completed": True}, headers=headers)
    client.post("/tasks/", json={"title": "Task 3", "priority": 2}, headers=headers)

    response = client.get("/tasks/stats", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
