from datetime import datetime
from pydantic import BaseModel


class SPostGetAll(BaseModel):
    limit: int | None = None
    offset: int | None = None


class SPostAdd(BaseModel):
    title: str
    description: str
    event_date: str
    is_active: bool = True


class SPost(BaseModel):
    post_id: int
    title: str
    # picture:
    description: str
    is_active: bool
    event_date: datetime
    created_at: datetime
    updated_at: datetime


class SPostPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    event_date: str | None = None
    is_active: bool | None = None
