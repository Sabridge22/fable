# базовый образ с Python
FROM python:3.14-slim

# устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь код приложения
COPY . .

# команда для запуска приложения
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]