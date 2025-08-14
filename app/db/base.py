# app/db/base.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Створюємо асинхронний двигун для підключення до БД
engine = create_async_engine(
    settings.database_url,
    echo=True,  # лог SQL у консоль (вимкнути на проді)
    future=True
)

# Створюємо фабрику сесій
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовий клас для всіх моделей
Base = declarative_base()

# Залежність для FastAPI — отримає сесію та закриє її після використання
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
