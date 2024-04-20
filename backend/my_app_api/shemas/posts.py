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


class SPost(BaseModel):
    post_id: int
    title: str
    # picture:
    description: str
    event_date: datetime
    created_at: datetime
