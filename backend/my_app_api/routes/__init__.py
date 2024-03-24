import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware

from my_app_api import __version__
from my_app_api.settings import get_settings

from .touch import router as touch_router


settings = get_settings()
logger = logging.getLogger(__name__)
app = FastAPI(
    title='Мое приложение',
    description='Бэкэнд приложения-примера',
    version=__version__,
    # Отключаем нелокальную документацию
    root_path=settings.ROOT_PATH if __version__ != 'dev' else '',
    docs_url='/swagger',
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

if settings.UI_DIR_PATH:
    logger.debug("Enabling UI")
    app.mount("/ui", app=StaticFiles(directory=settings.UI_DIR_PATH, html=True), name="ui")

if settings.DOCS_DIR_PATH:
    logger.debug("Enabling Docs")
    app.mount("/docs", app=StaticFiles(directory=settings.DOCS_DIR_PATH, html=True), name="docs")

app.include_router(touch_router)
