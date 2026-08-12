import httpx
from .config import BotConfig

class APIClient:
    @staticmethod
    async def register(email: str, password: str):
        username = email.split("@")[0]
        async with httpx.AsyncClient() as client:
            return await client.post(
                BotConfig.REGISTER_URL,
                json={"username": username, "email": email, "password": password}
            )
    @staticmethod
    async def login(email: str, password: str):
        async with httpx.AsyncClient() as client:
            return await client.post(
                BotConfig.LOGIN_URL,
                data={"username": email, "password": password}
            )

    @staticmethod
    async def send_message(token: str, content: str):
        async with httpx.AsyncClient() as client:
            return await client.post(
                BotConfig.CHAT_URL,
                json={"content": content},
                headers={"Authorization": f"Bearer {token}"}
            )