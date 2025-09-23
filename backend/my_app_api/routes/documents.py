import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from my_app_api.models.db_editor import Document, EditorDocument, AdminDocument, FileType, AdminFileType, get_db
from my_app_api.schemas.models import DocumentResponse, UserResponse
from my_app_api.utils.auth import get_current_user

from my_app_api.settings import get_settings

settings = get_settings()

document = APIRouter(prefix="/documents", tags=["documents"])


def get_file_type(filename: str) -> FileType:
    """Определяем тип файла по расширению"""
    ext = filename.lower().split('.')[-1]
    try:
        return FileType(ext)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Неподдерживаемый тип файла: {ext}"
        )

def validate_file(file: UploadFile) -> bool:
    """Проверяем файл на допустимость"""
    if not file.filename:
        return False
    filename = file.filename.lower()
    file_extension = f".{filename.split('.')[-1]}"
    return file_extension in settings.ALLOWED_EXTENSIONS

@document.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not file.filename or not validate_file(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый тип файла. Разрешенные типы: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Файл слишком большой. Максимальный размер: {settings.MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    file_extension = f".{file.filename.split('.')[-1]}"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    try:
        file_type = get_file_type(file.filename)
        
        document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            file_size=len(contents),
            file_type=file_type,
            uploaded_by_id=current_user.id,
            path=file_path,
            description=description
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return DocumentResponse
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении документа: {str(e)}"
        )


@document.get("/")
async def get_user_documents(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все документы пользователя"""
    documents = db.query(Document).filter(
        Document.uploaded_by_id == current_user.id
    ).order_by(Document.uploaded_at.desc()).all()
    
    return documents


@document.get("/{document_id}")
async def get_document(
    document_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить конкретный документ"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.uploaded_by_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден"
        )
    
    return document


@document.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить документ"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.uploaded_by_id == current_user.id
    ).first()
    
    if not document:
        raise Ob
    
    try:
        if os.path.exists(document.path):
            os.remove(document.path)
        
        db.delete(document)
        db.commit()
        
        return {"message": "Документ успешно удален"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении документа: {str(e)}"
        )