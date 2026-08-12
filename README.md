# AI-репетитор английского языка

Бэкенд-сервис для изучения английского языка через чат с нейросетью
Можно вместо изучения английского вписать любой промпт, и чат с нейросетью сможет использоваться для других целей 
---

## Возможности

- **Чат с Gemini AI** - диалог на английском с исправлением ошибок
- **JWT-аутентификация** - регистрация, вход, защита эндпоинтов
- **История сообщений** - все диалоги сохраняются в БД
- **Docker-контейнеризация** - лёгкий запуск в любой среде
- **Миграции через Alembic** - безопасное изменение структуры БД
- **Чистая архитектура** - слои: репозитории -> сервисы -> роутеры
- **Написаны тесты** - проект покрыт тестами для проверки основной логики и безопасности
- **Реализован Телеграм бот на aiogram** - бот работает через API и использует те же эндпоинты, что и веб-клиент. Он не имеет своей базы данных - все данные хранятся в основной БД


## Как это работает

1. **Пользователь регистрируется** - создаёт аккаунт с email и паролем.
2. **Входит в систему** - получает JWT-токен для авторизации.
3. **Начинает диалог** - отправляет сообщение через эндпоинт `/chat`.
4. **Сервер обрабатывает запрос**:
   - Сохраняет сообщение пользователя в базу данных.
   - Формирует контекст диалога (историю сообщений).
   - Отправляет запрос в **Gemini API** (Google AI).
   - Получает ответ, сохраняет его в БД и возвращает пользователю.
5. **Пользователь может посмотреть историю** - все диалоги сохраняются и доступны через эндпоинт `/chat/history`.

## Технологии

- **Python** 3.14+
- **FastAPI** - веб-фреймворк
- **PostgreSQL** + **SQLAlchemy** - БД
- **Alembic** - миграции
- **JWT** - аутентификация
- **Gemini API** - генерация ответов
- **Docker** + **Docker Compose** - контейнеризация
- **Pydantic** - валидация данных
- **Logging** - логирование
- **Pytest** - тестирование
- **Aiogram** - телеграм бот

---
## Быстрый запуск с Docker

### 1. Клонировать репозиторий
```bash
git clone https://github.com/ваш-аккаунт/fade_chat.git
cd fade_chat
```
### 2. Создать файл .env по примеру с .env.example
```plaintext
DATABASE_URL=postgresql+psycopg://postgres:postgrespw@db:5432/chatdb
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

GEMINI_API_KEY=your_api_key
LOG_LEVEL=INFO

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgrespw
POSTGRES_DB=chatdb
POSTGRES_PORT=35432
```

### 3. Запуск командой
```bash
docker-compose up --build
```

Сервер запустится на http://localhost:8000
Swagger документация - http://localhost:8000/docs


### 4. Остановить
```bash
docker-compose down
```

## Локальный запуск без Docker

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

### Запуск тестов

```bash
pytest -v
```


Сервер запустится на http://localhost:8000
Swagger документация - http://localhost:8000/docs

## Telegram-бот

Проект включает в себя **Telegram-бота**, который является полноценным клиентом API. Пользователь может общаться с нейросетью прямо в Telegram, без необходимости открывать сайт.

### Возможности бота

- **Автоматическая регистрация** - бот создаёт аккаунт автоматически по `telegram_id`, без ввода email и пароля.
- **Общение через API** - все сообщения отправляются через API, история диалогов сохраняется в БД.
- **Индикатор «Печатает...»** - пользователь видит, что бот обрабатывает сообщение.
- **Поддержка контекста** - бот помнит историю диалога.

### Запуск бота

```bash
# Установить зависимости
pip install aiogram httpx python-dotenv

# Запустить бота (локально)
python -m bot.main
```

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
├── Dockerfile # Инструкция для сборки образа
├── docker-compose.yml # Оркестрация контейнеров (app + db)
tests/
├── conftest.py # Общие настройки и фикстуры
├── test_auth.py # Тесты аутентификации
├── test_users.py # Тесты пользователей
└── test_chat.py # Тесты чата
├── bot/ # Telegram-бот
│   ├── main.py # Точка входа
│   ├── config.py # Настройки
│   ├── api_client.py # Клиент для API
│   └── handlers.py # Обработчики команд
```

## Доступные эндпоинты
### Аутентификация (/auth)
POST /auth/login - вход по email и паролю, получение JWT-токена

GET /auth/me - получение данных текущего пользователя (требуется токен)

### Пользователи (/users)
POST /users/register - регистрация нового пользователя

GET /users/{user_id} - получение пользователя по ID

GET /users/username/{username} - получение пользователя по username

GET /users/email/{email} - получение пользователя по email

PATCH /users/{user_id} - обновление профиля (только владелец)

DELETE /users/{user_id} - удаление профиля (только владелец)

GET /users - список всех пользователей (с пагинацией)

### Чат (/chat)
POST /chat - отправить сообщение нейросети (требуется токен)

GET /chat - получить историю диалога (требуется токен)

## Автор
GitHub: @Sabridge22