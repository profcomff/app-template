import starlette.requests
from starlette.responses import JSONResponse

from my_app_api.exceptions import (
    AlreadyExists,
    ObjectNotFound,
    TypeErrorCSV
)

from my_app_api.schemas.base import StatusResponseModel

from .base import app

@app.exception_handler(ObjectNotFound)
async def not_found_handler(req: starlette.requests.Request, exc: ObjectNotFound):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.eng, ru=exc.ru).model_dump(), status_code=404
    )


@app.exception_handler( AlreadyExists)
async def already_exists(req: starlette.requests.Request, exc: ObjectNotFound):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.eng, ru=exc.ru).model_dump(), status_code=409
    )


@app.exception_handler(TypeErrorCSV)
async def type_error_csv(req: starlette.requests.Request, exc: TypeErrorCSV):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.eng, ru=exc.ru).model_dump(), status_code=400
    )