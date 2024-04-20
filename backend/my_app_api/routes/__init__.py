import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_sqlalchemy import DBSessionMiddleware
from my_app_api import __version__
from my_app_api.settings import get_settings
from starlette.datastructures import URL

from .touch import router as touch_router
from .posts import router as posts_router
from my_app_api.orm.database import delete_tables, create_tables


async def lifespan(app: FastAPI):  # Дроп и создание БД при запуске приложения
    try:
        delete_tables()
        create_tables()
    except:
        pass
    yield
    delete_tables()

settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Мое приложение",
    description="Бэкэнд приложения-примера",
    version=__version__,
    # Отключаем нелокальную документацию
    root_path=settings.ROOT_PATH if __version__ != "dev" else "",
    docs_url="/swagger",
    redoc_url=None,
    lifespan=lifespan
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


@app.get("/")
def redirect(request: Request):
    url = URL(
        path="/ui/",
        query=request.url.components.query,
        fragment=request.url.components.fragment,
    )
    return RedirectResponse(url)


# app.include_router(touch_router)
app.include_router(posts_router)
