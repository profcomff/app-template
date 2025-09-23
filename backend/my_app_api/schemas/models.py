from datetime import date, datetime
from uuid import UUID
from typing import Optional, Dict, List
from pydantic import EmailStr, validator

from .base import Base
from my_app_api.models import Role


class UserBase(Base):
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
    user_login: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    

class DocumentResponse(Base):

class DocumentResponse(DocumentBase):
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    uploaded_at: datetime


class DatabaseCreate(Base):
    csv_file: str
    year: int
    column_mapping: Dict[str, str]
    table_name: Optional[str] = None


class DatabaseResponse(Base):
    db_name: str
    original_filename: str
    year: int
    table_name: str
    created_at: datetime