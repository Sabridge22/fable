import os
from dotenv import load_dotenv

load_dotenv()

class BotConfig:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    API_BASE_URL = os.getenv("API_BASE_URL")
    PASSWORD_SALT = os.getenv("PASSWORD_SALT")

    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")

    # эндпоинты
    REGISTER_URL = f"{API_BASE_URL}/users/register"
    LOGIN_URL = f"{API_BASE_URL}/auth/login"
    CHAT_URL = f"{API_BASE_URL}/chat/"