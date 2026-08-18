# тесты для регистрации, обновления и удаления пользователей

from sqlalchemy import select

from app.models.message import MessageORM


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


def test_delete_user_with_history_success(client, auth_token, db_session):
    """удаление пользователя с историей сообщений, 204 + каскадное удаление"""
    user_id = get_user_id(client, auth_token)

    # вставляем сообщение напрямую в БД, минуя вызов LLM
    db_session.add(MessageORM(user_id=user_id, content="Hello!", role="user"))
    db_session.commit()

    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204

    # сообщения удалены каскадом вместе с пользователем
    remaining = db_session.execute(
        select(MessageORM).where(MessageORM.user_id == user_id)
    ).scalar_one_or_none()
    assert remaining is None


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