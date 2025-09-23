from __future__ import annotations

import datetime
from enum import Enum

from sqlalchemy import  Boolean, Date, Integer, String, Text, Numeric, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel



class Role(str, Enum):
    USER: str = "user"
    EDITOR: str = "editor"
    ADMIN: str = "admin"


class User(BaseDbModel):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.now)

    rule: Mapped[User] = mapped_column(Enum(Role, native_enum=False), nullable=False)
    

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


class Evacuations(BaseDbModel):
    __tablename__ = 'evacuations_data'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    
    tow_trucks_online: Mapped[int] = mapped_column(Integer, nullable=False)
    dispatches_count: Mapped[int] = mapped_column(Integer, nullable=False)
    evacuations_count: Mapped[int] = mapped_column(Integer, nullable=False)
    parking_receipts: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)


class EvacuationRoute(BaseDbModel):
    __tablename__ = 'evacuation_routes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    
    route_description: Mapped[str] = mapped_column(Text, nullable=False)
    route_path: Mapped[str] = mapped_column(Text)
    

    evacuations = relationship("EvacuationsData", 
                             primaryjoin="and_(EvacuationsData.year == EvacuationRoute.year, "
                                        "EvacuationsData.month == EvacuationRoute.month)")


class TrafficLight(BaseDbModel):
    __tablename__ = 'traffic_lights'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    light_type: Mapped[str] = mapped_column(String(10), nullable=False)
    installation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    worked: Mapped[bool] = mapped_column(Boolean, nullable=True)


