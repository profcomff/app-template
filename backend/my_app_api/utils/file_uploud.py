import os
import uuid
import pandas as pd

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from my_app_api.exceptions import ObjectNotFound, AlreadyExists, TypeErrorCSV
from my_app_api.settings import get_settings


settings = get_settings()


async def save_uploaded_file(file: UploadFile, upload_dir: str, allowed_extensions: list) -> str:
    content = await file.read()
    
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, upload_dir, filename)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
     
    with open(file_path, "wb") as f:
        f.write(content)
    
    return filename

# Функция для загрузки документов (PDF, Word, Excel)
async def upload_document(file: UploadFile) -> dict:
    allowed_extensions = ['.pdf', '.doc', '.docx']
    
    filename = await save_uploaded_file(
        file,
        "documents",
        allowed_extensions
    )
    
    file_path = os.path.join(settings.UPLOAD_DIR, "documents", filename)
    file_size = os.path.getsize(file_path)
    
    return {
        "filename": filename,
        "original_name": file.filename,
        "file_size": file_size,
        "uploaded_at": datetime.now()
    }
