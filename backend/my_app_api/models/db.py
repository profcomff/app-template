from __future__ import annotations

import uuid
import datetime
from enum import Enum
from typing import List

from sqlalchemy import  Boolean, Date, Integer, String, Text, Numeric, Enum as SQLEnum, DateTime, UUID, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel
from .db_editor import Document



class Role(str, Enum):
    EDITOR: str = "editor"
    ADMIN: str = "admin"


class User(BaseDbModel):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)  # Добавлена длина
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(100), nullable=True)  # Добавлена длина
    user_login: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hashed: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[Role] = mapped_column(SQLEnum(Role, native_enum=False), nullable=False)

    documents: Mapped[List["Document"]] = relationship("Document", back_populates="uploaded_by")
    

class FinesData(BaseDbModel):
    __tablename__ = 'fines_data'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    
    violations_count: Mapped[int] = mapped_column(Integer, nullable=False)
    decrees_count: Mapped[int] = mapped_column(Integer, nullable=False)
    fines_imposed: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    fines_collected: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)


class EvacuationRoute(BaseDbModel):
    __tablename__ = 'evacuation_routes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    route_path: Mapped[str] = mapped_column(Text)
    
    evacuations: Mapped[List["Evacuations"]] = relationship("Evacuations", back_populates="route")

class Evacuations(BaseDbModel):
    __tablename__ = 'evacuations'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    
    route_id: Mapped[int] = mapped_column(ForeignKey('evacuation_routes.id'), nullable=True)
    
    evacuators_count: Mapped[int] = mapped_column(Integer, nullable=False)
    call_count: Mapped[int] = mapped_column(Integer, nullable=False)
    evacuations_count: Mapped[int] = mapped_column(Integer, nullable=False)
    collected_sum: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)

    route: Mapped[EvacuationRoute] = relationship("EvacuationRoute", back_populates="evacuations")


class TrafficLight(BaseDbModel):
    __tablename__ = 'traffic_lights'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    light_type: Mapped[str] = mapped_column(String(10), nullable=False)
    installation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    worked: Mapped[bool] = mapped_column(Boolean, nullable=True)

