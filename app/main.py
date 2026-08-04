from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.core.config import settings
from app.models.base import Base

from app.api.routers.user import router as user_router
from app.api.routers.auth import router as auth_router
from app.api.routers.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Создание таблиц...')
    print(f'Таблицы: {list(Base.metadata.tables.keys())}')
    Base.metadata.create_all(bind=engine)
    print('Таблицы созданы')
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=user_router)
app.include_router(router=auth_router)
app.include_router(router=chat_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOWED_ORIGINS,
    allow_methods = ["*"],
)