import hashlib
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from .api_client import APIClient
from .config import BotConfig


user_tokens = {}  # {telegram_id: token}

def generate_email(telegram_id: int) -> str:
    return f"telegram_{telegram_id}@fade.chat"

def generate_password(telegram_id: int) -> str:
    return hashlib.sha256(f"{telegram_id}{BotConfig.PASSWORD_SALT}".encode()).hexdigest()[:16]

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    email = generate_email(telegram_id)
    password = generate_password(telegram_id)

    # регистрация
    reg_resp = await APIClient.register(email, password)
    if reg_resp.status_code not in (201, 409):
        await message.answer("Ошибка регистрации")
        return

    # логин
    login_resp = await APIClient.login(email, password)
    if login_resp.status_code != 200:
        await message.answer("Ошибка входа")
        return

    token = login_resp.json()["access_token"]
    user_tokens[telegram_id] = token

    await message.answer(
        "Добро пожаловать!\n"
        "Теперь просто пиши сообщения на английском, и мы начнем обучение."
    )

@router.message()
async def handle_text(message: Message):
    telegram_id = message.from_user.id
    token = user_tokens.get(telegram_id)

    if not token:
        await message.answer("Сначала нажми /start")
        return

    thinking_msg = await message.answer("Печатаю...")

    try:
        resp = await APIClient.send_message(token, message.text)
        try:
            await thinking_msg.delete()
        except Exception:
            pass
        
        if resp.status_code == 200:
            data = resp.json()
            await message.answer(data["content"])
        else:
            await message.answer("Ошибка. Попробуйте позже.")
    except Exception as e:
        try:
            await thinking_msg.delete()
        except Exception:
            pass
        await message.answer("Ошибка. Попробуйте позже.")