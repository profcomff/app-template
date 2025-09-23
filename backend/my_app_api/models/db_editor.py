from __future__ import annotations

import datetime
from enum import Enum
from typing import Dict, Any

from sqlalchemy import Integer, String, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel
from .db import User


class FileType(str, Enum):
    PDF: str = 'pdf'
    DOC: str = 'doc'
    DOCX: str = 'docx'


class AdminFileType(str, Enum):
    PDF: str = 'pdf'
    DOC: str = 'doc'
    DOCX: str = 'docx'
    CSV: str = 'csv'
    XLSX: str = 'xlsx'
    XLS: str = 'xls'


class Document(BaseDbModel):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    
    uploaded_by: Mapped[User] = relationship("User", back_populates="documents")

class EditorDocument(Document):
    __tablename__ = 'editor_documents'
    
    id: Mapped[int] = mapped_column(ForeignKey('base_documents.id'), primary_key=True)
    file_type: Mapped[FileType] = mapped_column(SQLEnum(FileType, native_enum=False), nullable=False)


class AdminDocument(Document):
    __tablename__ = 'admin_documents'
    
    id: Mapped[int] = mapped_column(ForeignKey('base_documents.id'), primary_key=True)
    file_type: Mapped[AdminFileType] = mapped_column(SQLEnum(AdminFileType, native_enum=False), nullable=False)


class Sections(BaseDbModel):
    __tablename__ = 'sections'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    section_type: Mapped[str] = mapped_column(String(50), nullable=True)


class Posts(BaseDbModel):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    section_id: Mapped[int] = mapped_column(ForeignKey('sections.id'), nullable=True)
    contents: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    
    uploaded_by: Mapped["User"] = relationship("User")
    section: Mapped[Sections] = relationship("Sections", back_populates="posts")