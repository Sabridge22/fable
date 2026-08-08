from google import genai
from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "models/gemini-3.1-flash-lite"

    def generate_response(self, context: list[dict]) -> str:
        try:
            history = []
            for msg in context:
                history.append({
                    "role": msg["role"],
                    "parts": [{"text": msg["parts"]}]
                })
            response = self.client.models.generate_content(
                model=self.model,
                contents=history
            )
            return response.text
        except Exception as e:
            print(f"LLM API error: {e}")
            return "Извините, сейчас я не могу ответить. Попробуйте позже."