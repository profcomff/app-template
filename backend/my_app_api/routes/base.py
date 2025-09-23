from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from logger_middleware import LoggerMiddleware

from my_app_api import __version__
from my_app_api.routes.admin import admin
from my_app_api.routes.editor import editor
from my_app_api.routes.documents import documents
from my_app_api.routes.auth import auth
from my_app_api.settings import Settings, get_settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


settings: Settings = get_settings()
app = FastAPI(
    title='Сайт ЦОДД',
    description='Что-то с чем-то.',
    version=__version__,
    root_path=settings.ROOT_PATH if __version__ != 'dev' else '/',
    docs_url=None if __version__ != 'dev' else '/docs',
    redoc_url=None,
)

app.add_middleware(
    DBSessionMiddleware,
    db_url=str(settings.DB_DSN),
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(admin)
app.include_router(editor)
app.include_router(documents)
app.include_router(auth)

if __version__ != 'dev':
    app.add_middleware(LoggerMiddleware, service_id=settings.SERVICE_ID)
