from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import JSON, Column, Integer


class Model(DeclarativeBase):
    pass

# Создаем базу данных


class PostOrm(Model):
    __tablename__ = 'post'
    post_id: Mapped[int] = mapped_column(primary_key=True)

    # Extra columns
    title: Mapped[str]
    picture_id: Mapped[int]
    description: Mapped[str]
    event_date: Mapped[datetime]
    is_active: Mapped[bool]

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())"),
        onupdate=datetime.utcnow)


class ReactionOrm(Model):
    __tablename__ = 'reaction'
    reaction_id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int]
    reaction: Mapped[int]
