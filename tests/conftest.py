import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.models.base import Base


# тестовая бд
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# переопределяем зависимость get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# фикстура: сессия БД для прямого доступа к данным
@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# фикстура: клиент для тестов
@pytest.fixture
def client():
    # создаём таблицы перед тестом
    Base.metadata.create_all(bind=engine)
    
    # создаём тестовый клиент
    yield TestClient(app)
    
    # удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)


# фикстура: создание тестового пользователя и получение токена
@pytest.fixture
def auth_token(client):
    # создаёт пользователя и возвращает JWT токен для авторизации
    
    # регистрируем пользователя
    client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    # логинимся
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    
    return response.json()["access_token"]
