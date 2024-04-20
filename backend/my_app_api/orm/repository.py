from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

from my_app_api.settings import get_settings
from my_app_api.models.models_db import Model

settings = get_settings()


engine = create_engine(settings.DB_DSN)  # Движок БД

new_session = sessionmaker(engine)  # Сессия для работы с БД


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
