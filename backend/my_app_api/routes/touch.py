import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/example", tags=["Example"])

CLICKS: dict[int, int] = {}


class WhoAmI(BaseModel):
    id: int


class TouchGet(WhoAmI):
    count: int


# region routes
@router.get("/whoami", response_model=WhoAmI)
def whoami(auth=Depends(UnionAuth(allow_none=False))):
    return {"id": auth["id"]}


@router.post("/touch", response_model=TouchGet)
def touch(auth=Depends(UnionAuth(allow_none=False))):
    if auth["id"] not in CLICKS:
        CLICKS[auth["id"]] = 0
    CLICKS[auth["id"]] += 1
    return {"id": auth["id"], "count": CLICKS[auth["id"]]}


# endregion
