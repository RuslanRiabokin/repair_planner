# scripts/create_tables.py

import asyncio
import logging

# Імпортуємо тут моделі, щоб вони зареєструвались в Base.metadata
import app.db.models  # noqa: F401

from app.db.base import engine, Base


async def create_tables() -> None:
    """
    Створює всі таблиці, визначені в metadata (для dev).
    Увага: це простий підхід для локальної розробки.
    Для продакшн використовуй Alembic-міграції.
    """
    async with engine.begin() as conn:
        logging.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Tables created.")
    await engine.dispose()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(create_tables())
    print("Done.")
