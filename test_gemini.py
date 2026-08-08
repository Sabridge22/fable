from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Попробуй по очереди эти модели
response = client.models.generate_content(
    model="models/gemini-3.1-flash-lite",  # или gemini-2.0-flash-lite
    contents="Say 'Hello, Gemini!' in Russian"
)
print(response.text)