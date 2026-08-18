from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging

from app.api.routers.user import router as user_router
from app.api.routers.auth import router as auth_router
from app.api.routers.chat import router as chat_router


setup_logging(settings.LOG_LEVEL)

app = FastAPI()
app.include_router(router=user_router)
app.include_router(router=auth_router)
app.include_router(router=chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
)