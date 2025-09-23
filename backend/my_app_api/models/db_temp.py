from __future__ import annotations

import uuid
import datetime
from enum import Enum

from sqlalchemy import  Boolean, Date, Integer, String, Text, Numeric, Enum, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel

class Status(str, Enum):
    PENDING: str = "pending"
    APPROVED: str = "approved"
    REJECTED: str = "rejected"


class FinesDataTemp(BaseDbModel):
    __tablename__ = 'fines_data_temp'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    
    violations_count: Mapped[int] = mapped_column(Integer, nullable=False)
    decrees_count: Mapped[int] = mapped_column(Integer, nullable=False)
    fines_imposed: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    fines_collected: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    
    import_batch: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    imported_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    status: Mapped[Status] = mapped_column(Enum(Status, native_enum=False), default='pending')


class EvacuationsTemp(BaseDbModel):
    __tablename__ = 'evacuations_data_temp'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    
    tow_trucks_online: Mapped[int] = mapped_column(Integer, nullable=False)
    dispatches_count: Mapped[int] = mapped_column(Integer, nullable=False)
    evacuations_count: Mapped[int] = mapped_column(Integer, nullable=False)
    parking_receipts: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)

    import_batch: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    imported_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    status: Mapped[Status] = mapped_column(Enum(Status, native_enum=False), default='pending')


class EvacuationRouteTemp(BaseDbModel):
    __tablename__ = 'evacuation_routes_Temp'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    
    route_description: Mapped[str] = mapped_column(Text, nullable=False)
    route_path: Mapped[str] = mapped_column(Text)
    

    evacuations = relationship("EvacuationsData", 
                             primaryjoin="and_(EvacuationsData.year == EvacuationRoute.year, "
                                        "EvacuationsData.month == EvacuationRoute.month)")
    
    import_batch: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    imported_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    status: Mapped[Status] = mapped_column(Enum(Status, native_enum=False), default='pending')


class TrafficLightTemp(BaseDbModel):
    __tablename__ = 'traffic_lights_Temp'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    light_type: Mapped[str] = mapped_column(String(10), nullable=False)
    installation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    worked: Mapped[bool] = mapped_column(Boolean, nullable=True)

    import_batch: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    imported_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    status: Mapped[Status] = mapped_column(Enum(Status, native_enum=False), default='pending')