from datetime import datetime
from pydantic import BaseModel


class SPostGetAll(BaseModel):
    limit: int | None = None
    offset: int | None = None


class SPostAdd(BaseModel):
    title: str
    description: str
    event_date: str  # парсить в datetime
    is_active: bool = True
    picture_id: int | None = None


class SPost(BaseModel):
    post_id: int
    title: str
    # picture:
    description: str
    event_date: str
    created_at: datetime
