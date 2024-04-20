from datetime import datetime
from pydantic import BaseModel
from fastapi import UploadFile


class SPostGetAll(BaseModel):
    limit: int | None = None
    offset: int | None = None


class SPostAdd(BaseModel):
    title: str
    description: str
    event_date: str  # парсить в datetime
    picture: UploadFile | None = None
    is_active: bool = True


class SPost(BaseModel):
    post_id: int
    title: str
    # picture:
    description: str
    event_date: str
    created_at: datetime
