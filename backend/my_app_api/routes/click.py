import logging

from fastapi import APIRouter
from pydantic import BaseModel


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/click', tags=['Click'])


# region schemas
class ClickResponse(BaseModel):
    count: int


# endregion


# region routes
@router.get('')
def get_clicks() -> ClickResponse:
    return ClickResponse(count=1)


# endregion
