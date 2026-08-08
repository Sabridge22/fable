# AI-репетитор английского языка

Бэкенд-сервис для изучения английского языка через диалог с нейросетью.

---

## Возможности

- **Интеллектуальный чат с Gemini AI** — диалог на английском с исправлением ошибок
- **JWT-аутентификация** — регистрация, вход, защита эндпоинтов
- **История сообщений** — все диалоги сохраняются в БД
- **Чистая архитектура** — слои: репозитории -> сервисы -> роутеры

---

## Технологии

- **Python** 3.14+
- **FastAPI** — веб-фреймворк
- **PostgreSQL** + **SQLAlchemy** — БД
- **Alembic** — миграции
- **JWT** — аутентификация
- **Gemini API** — генерация ответов
- **Docker** — база данных (создание через контейнер)
- **Pydantic** — валидация данных
- **Logging** — логирование

---

## Старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/ваш-аккаунт/fade_chat.git
cd fade_chat
```

### 2. Создать виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Создать файл .env по примеру
```plaintext
DATABASE_URL=postgresql+psycopg://postgres:admin@localhost:35432/chatdb
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=your_gemini_api_key
LOG_LEVEL=INFO
```

### 5. Запустить PostgreSQL в Docker
```bash
docker run --name your_db_name -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=your_db_name -d -p 5432:5432 postgres
```

### 6. Применить миграции
```bash
alembic upgrade head
```

### 7. Запустить сервер
```bash
uvicorn app.main:app --reload
```

Сервер запустится на http://localhost:8000
Swagger документация — http://localhost:8000/docs

##  Структура проекта
```plaintext
fade_chat/
├── alembic/ # Миграции БД
├── app/
│ ├── api/
│ │ └── routers/ # Эндпоинты (auth, users, chat)
│ ├── core/ # Конфиг, JWT, логи
│ ├── db/ # Подключение к БД
│ ├── dependencies/ # get_current_user
│ ├── models/ # SQLAlchemy модели
│ ├── repositories/ # Работа с БД (CRUD)
│ ├── schemas/ # Pydantic схемы
│ └── services/ # Бизнес-логика
├── .env.example
├── requirements.txt
└── README.md
```

## Доступные эндпоинты
### Аутентификация (/auth)
POST /auth/login — вход по email и паролю, получение JWT-токена

GET /auth/me — получение данных текущего пользователя (требуется токен)

### Пользователи (/users)
POST /users/register — регистрация нового пользователя

GET /users/{user_id} — получение пользователя по ID

GET /users/username/{username} — получение пользователя по username

GET /users/email/{email} — получение пользователя по email

PATCH /users/{user_id} — обновление профиля (только владелец)

DELETE /users/{user_id} — удаление профиля (только владелец)

GET /users — список всех пользователей (с пагинацией)

### Чат (/chat)
POST /chat — отправить сообщение ИИ-репетитору (требуется токен)

GET /chat — получить историю диалога (требуется токен)

## Автор
GitHub: @Sabridge22