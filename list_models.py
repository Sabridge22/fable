from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Выведет список всех доступных моделей
for model in client.models.list():
    print(model.name)