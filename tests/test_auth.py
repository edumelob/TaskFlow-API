def test_register_new_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "novo@teste.com", "password": "senhaSegura123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "novo@teste.com"
    assert "id" in data
    assert "hashed_password" not in data  # nunca deve vazar a senha, nem com hash


def test_register_duplicate_email_fails(client, registered_user):
    response = client.post("/auth/register", json=registered_user)
    assert response.status_code == 400


def test_login_with_correct_credentials(client, registered_user):
    response = client.post(
        "/auth/login",
        data={"username": registered_user["email"], "password": registered_user["password"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_with_wrong_password_fails(client, registered_user):
    response = client.post(
        "/auth/login",
        data={"username": registered_user["email"], "password": "senhaErrada"},
    )
    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "usuario@teste.com"
