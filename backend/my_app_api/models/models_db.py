from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import JSON, Column, Integer


class Model(DeclarativeBase):
    pass
