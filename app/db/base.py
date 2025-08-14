# app/db/base.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Створюємо асинхронний engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Логи SQL-запитів у консоль
    future=True
)

# Фабрика сесій
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовий клас для моделей
Base = declarative_base()

# Дістаємо сесію (для dependency у FastAPI)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
