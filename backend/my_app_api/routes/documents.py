from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from ..database import get_db
from ..models import User, UserDocument
from ..schemas.models import DocumentResponse, DocumentCreate
from my_app_api.utils.auth import get_current_user
from ..utils.file_upload import process_document

documents = APIRouter(prefix="/documents", tags=["documents"])

@documents.post("/", response_model=DocumentResponse)
async def upload_document(
    description: str = None,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filename, file_size = await process_document(file)
    
    document = UserDocument(
        user_id=current_user.id,
        filename=filename,
        original_filename=file.filename,
        file_path=f"app/static/documents/{filename}",
        file_size=file_size,
        file_type=file.content_type,
        description=description
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document

@documents.get("/", response_model=List[DocumentResponse])
def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user.documents

@documents.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document = db.query(UserDocument).filter(
        UserDocument.id == document_id,
        UserDocument.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@documents.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document = db.query(UserDocument).filter(
        UserDocument.id == document_id,
        UserDocument.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Удаление файла
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}