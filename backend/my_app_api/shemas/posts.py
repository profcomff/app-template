from datetime import datetime
from pydantic import BaseModel


class SPostGetAll(BaseModel):
    limit: int | None = None
    offset: int | None = None


class SPostAdd(BaseModel):
    title: str
    descriprion: str
    event_date: str  # парсить в datetime
    # picture: str | None = None


class SPost(BaseModel):
    post_id: int
    title: str
    # picture:
    descriprion: str
    event_date: datetime
    created_at: datetime
