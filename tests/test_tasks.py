def test_create_task(client, auth_headers):
    response = client.post(
        "/tasks/",
        json={"title": "Estudar FastAPI", "description": "Revisar autenticação JWT"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Estudar FastAPI"
    assert data["is_completed"] is False


def test_list_tasks_requires_auth(client):
    response = client.get("/tasks/")
    assert response.status_code == 401


def test_list_tasks_returns_only_own_tasks(client, auth_headers):
    client.post("/tasks/", json={"title": "Tarefa 1"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Tarefa 2"}, headers=auth_headers)

    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_task(client, auth_headers):
    created = client.post("/tasks/", json={"title": "Antiga"}, headers=auth_headers).json()

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"is_completed": True},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["is_completed"] is True
    assert response.json()["title"] == "Antiga"  # campo não enviado permanece igual


def test_delete_task(client, auth_headers):
    created = client.post("/tasks/", json={"title": "Remover"}, headers=auth_headers).json()

    response = client.delete(f"/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 204

    check = client.get(f"/tasks/{created['id']}", headers=auth_headers)
    assert check.status_code == 404


def test_user_cannot_access_tasks_from_another_user(client):
    # Usuário A cria uma tarefa
    client.post("/auth/register", json={"email": "a@teste.com", "password": "senhaSegura123"})
    token_a = client.post(
        "/auth/login", data={"username": "a@teste.com", "password": "senhaSegura123"}
    ).json()["access_token"]
    task = client.post(
        "/tasks/",
        json={"title": "Tarefa do usuário A"},
        headers={"Authorization": f"Bearer {token_a}"},
    ).json()

    # Usuário B tenta acessar a tarefa do usuário A
    client.post("/auth/register", json={"email": "b@teste.com", "password": "senhaSegura123"})
    token_b = client.post(
        "/auth/login", data={"username": "b@teste.com", "password": "senhaSegura123"}
    ).json()["access_token"]

    response = client.get(
        f"/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert response.status_code == 404
