# тесты для регистрации, обновления и удаления пользователей

def test_register_success(client):
    """успешная регистрация"""
    response = client.post(
        "/users/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "pass123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data

def test_register_dublicate_email(client):
    """регистрация с уже занятым email, 409 Conflict"""

    client.post(
        "/users/register",
        json={
            "username": "user1",
            "email": "duplicate@example.com",
            "password": "pass123"
        }
    )

    response = client.post(
        "/users/register",
        json={
            "username": "user2",
            "email": "duplicate@example.com",
            "password": "pass123"
        }
    )

    assert response.status_code == 409


def test_register_duplicate_username(client):
    """регистрация с уже занятым username, 409 Conflict"""
    client.post("/users/register", json={
        "username": "sameuser",
        "email": "test1@example.com",
        "password": "pass123"
    })
    
    response = client.post("/users/register", json={
        "username": "sameuser",
        "email": "test2@example.com",
        "password": "pass123"
    })
    
    assert response.status_code == 409


def get_user_id(client, token):
    """вспомогательная функция, получает id текущего пользователя"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()["id"]


def test_update_user_success(client, auth_token):
    """обновление своего профиля, успех"""
    user_id = get_user_id(client, auth_token)
    
    response = client.patch(
        f"/users/{user_id}",
        json={"username": "updated_name"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["username"] == "updated_name"


def test_update_user_forbidden(client, auth_token):
    """попытка обновить чужой профиль, 403 Forbidden"""
    # создаём второго пользователя
    client.post("/users/register", json={
        "username": "otheruser",
        "email": "other@example.com",
        "password": "pass123"
    })
    
    # логинимся как второй пользователь
    login_response = client.post(
        "/auth/login",
        data={"username": "other@example.com", "password": "pass123"}
    )
    other_token = login_response.json()["access_token"]
    
    user_id = get_user_id(client, auth_token)
    
    response = client.patch(
        f"/users/{user_id}",
        json={"username": "hacked"},
        headers={"Authorization": f"Bearer {other_token}"}
    )
    
    assert response.status_code == 403


def test_delete_user_success(client, auth_token):
    """удаление своего профиля, 204 No Content"""
    user_id = get_user_id(client, auth_token)
    
    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 204


def test_delete_user_forbidden(client, auth_token):
    """попытка удалить чужой профиль, 403 Forbidden"""
    # создаём второго пользователя
    client.post("/users/register", json={
        "username": "otheruser2",
        "email": "other2@example.com",
        "password": "pass123"
    })
    
    login_response = client.post(
        "/auth/login",
        data={"username": "other2@example.com", "password": "pass123"}
    )
    other_token = login_response.json()["access_token"]
    
    user_id = get_user_id(client, auth_token)
    
    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {other_token}"}
    )
    
    assert response.status_code == 403