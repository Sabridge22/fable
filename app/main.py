from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.core.config import settings
from app.models.base import Base



@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Создание таблиц...')
    print(f'Таблицы: {list(Base.metadata.tables.keys())}')
    Base.metadata.create_all(bind=engine)
    print('Таблицы созданы')
    yield


app = FastAPI(lifespan=lifespan)


app.middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOWED_ORIGINS,
    allow_methods = ["*"],
)