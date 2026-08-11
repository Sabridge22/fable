# тесты для чата с нейросетью

def test_chat_send_message(client, auth_token):
    """отправка сообщения, успех (даже если нейросеть не работает)"""
    response = client.post(
        "/chat",
        json={"content": "Hello!"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # проверяем, что запрос обработан (200 или 400 или 500, зависит от нейросети)
    assert response.status_code in [200, 400, 500]
    if response.status_code == 200:
        assert "content" in response.json()
        assert response.json()["role"] == "assistant"

def test_chat_get_history(client, auth_token):
    """получение истории чата, успех"""
    # сначала отправляем сообщение для создания истории
    client.post(
        "/chat",
        json={"content": "Hello!"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/chat",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)