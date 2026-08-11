# тесты для аутентификации

def test_login_success(client):
    """успешный логин, возвращается токен"""

    client.post("/users/register", json={
        "username": "logintest",
        "email": "login@example.com",
        "password": "pass123"
    })

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "pass123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """неверный пароль, 401 Unauthorized"""

    client.post("/users/register", json={
        "username": "wrongpass",
        "email": "wrong@example.com",
        "password": "correctpass"
    })

    response = client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401

def test_login_user_not_found(client):
    """пользователь не найден, 401 Unauthorized"""

    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "anything"
        }
    )

    assert response.status_code == 401

def test_me_endpoint(client, auth_token):
    """получение текущего пользователя по токену, возвращаются данные"""

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
