from datetime import date, datetime
from uuid import UUID
from typing import Optional, List
from pydantic import EmailStr, validator

from .base import Base
from my_app_api.models import Role, Status


class FinesDataBase(Base):
    date: date
    year: int
    month: int
    violations_count: int
    decrees_count: int
    fines_imposed: float
    fines_collected: float


class EvacuationsBase(Base):
    date: date
    year: int
    month: int
    tow_trucks_online: int
    dispatches_count: int
    evacuations_count: int
    parking_receipts: float


class EvacuationRouteBase(Base):
    year: int
    month: int
    route_description: str
    route_path: Optional[str] = None


class TrafficLightBase(Base):
    address: str
    light_type: str
    installation_year: int
    worked: Optional[bool] = None


class FinesDataTempBase(FinesDataBase):
    import_batch: UUID
    imported_at: datetime
    status: Status

class EvacuationsTempBase(EvacuationsBase):
    import_batch: UUID
    imported_at: datetime
    status: Status

class EvacuationRouteTempBase(EvacuationRouteBase):
    import_batch: UUID
    imported_at: datetime
    status: Status

class TrafficLightTempBase(TrafficLightBase):
    import_batch: UUID
    imported_at: datetime
    status: Status


class UserBase(Base):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: Role

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserLogin(Base):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(Base):
    access_token: str
    token_type: str

class TokenData(Base):
    user_id: Optional[int] = None

# Profile schemas
class ProfileBase(Base):
    phone: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    avatar: Optional[str] = None
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Document schemas
class DocumentBase(Base):
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# Order schemas
class OrderItemBase(Base):
    product_name: str
    quantity: int
    price: float

class OrderItemResponse(OrderItemBase):
    id: int
    
    class Config:
        from_attributes = True

class OrderBase(Base):
    total_amount: float

class OrderResponse(OrderBase):
    id: int
    order_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

# Support schemas
class SupportTicketBase(Base):
    subject: str
    description: str
    priority: str = "medium"

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicketResponse(SupportTicketBase):
    id: int
    ticket_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SupportMessageBase(Base):
    message: str

class SupportMessageCreate(SupportMessageBase):
    pass

class SupportMessageResponse(SupportMessageBase):
    id: int
    user_id: int
    is_from_support: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Settings schemas
class SettingsBase(Base):
    email_notifications: bool = True
    sms_notifications: bool = False
    language: str = "ru"
    theme: str = "light"
    timezone: str = "Europe/Moscow"

class SettingsResponse(SettingsBase):
    updated_at: datetime
    
    class Config:
        from_attributes = True