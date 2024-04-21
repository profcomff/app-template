from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from my_app_api.settings import get_settings
from my_app_api.models.models_db import Model

settings = get_settings()


engine = create_async_engine(url=settings.database_url_asyncpg)

new_session = async_sessionmaker(engine)  # Сессия для работы с БД


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


# def create_tables():
#     Model.metadata.create_all(engine)


# def delete_tables():
#     Model.metadata.drop_all(engine)
