from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
import pandas as pd
import tempfile
import os

from database.manager import db_manager
from schemas.models import *

database = APIRouter(prefix="/database", tags=["database"])

@database.post("/databases/analyze-columns/")
async def analyze_csv_columns(file: UploadFile = File(...)):
    """Анализирует колонки CSV файла"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files supported")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        columns = db_manager.analyze_csv_columns(tmp_path)
        
        # Читаем sample данных для предпросмотра
        df = pd.read_csv(tmp_path, nrows=5)
        sample_data = df.head(3).to_dict('records')
        
        return {
            "columns": columns,
            "sample_data": sample_data,
            "total_rows": len(pd.read_csv(tmp_path))
        }
    finally:
        os.unlink(tmp_path)

@database.post("/databases/", response_model=Dict)
async def create_database(
    year: int,
    table_name: Optional[str] = None,
    file: UploadFile = File(...)
):
    """Создает новую БД из CSV файла"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files supported")
    
    # В реальном приложении получаем user_id из JWT токена
    user_id = 1  # Заглушка
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Анализируем колонки (в реальном приложении mapping приходит с фронта)
        columns = db_manager.analyze_csv_columns(tmp_path)
        column_mapping = {col: db_manager.sanitize_name(col) for col in columns}
        
        db_name = db_manager.create_database_from_csv(
            csv_file=tmp_path,
            year=year,
            user_id=user_id,
            column_mapping=column_mapping,
            table_name=table_name
        )
        
        return {
            "status": "success",
            "db_name": db_name,
            "message": f"Database {db_name} created successfully"
        }
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        os.unlink(tmp_path)

@database.get("/databases/", response_model=List[DatabaseResponse])
async def list_databases(year: Optional[int] = None):
    """Возвращает список всех баз данных"""
    databases = db_manager.list_databases(year)
    return databases

@database.delete("/databases/{db_name}")
async def delete_database(db_name: str):
    """Удаляет базу данных"""
    try:
        user_id = 1  # Заглушка - из JWT токена
        db_manager.delete_database(db_name, user_id)
        return {"status": "success", "message": f"Database {db_name} deleted"}
    except Exception as e:
        raise HTTPException(400, str(e))

@database.get("/databases/{db_name}/data")
async def get_database_data(db_name: str, limit: int = 100, offset: int = 0):
    """Возвращает данные из указанной базы"""
    try:
        db_entry = db_manager.session.query(DatabaseRegistry).filter(
            DatabaseRegistry.db_name == db_name
        ).first()
        
        if not db_entry:
            raise HTTPException(404, "Database not found")
        
        engine = create_engine(
            f'postgresql+psycopg2://{settings.pg_user}:{settings.pg_password}@'
            f'{settings.pg_host}:{settings.pg_port}/{db_name}'
        )
        
        df = pd.read_sql(f"SELECT * FROM {db_entry.table_name} LIMIT {limit} OFFSET {offset}", engine)
        
        return {
            "db_name": db_name,
            "table_name": db_entry.table_name,
            "columns": df.columns.tolist(),
            "data": df.to_dict('records'),
            "total_returned": len(df)
        }
    except Exception as e:
        raise HTTPException(500, str(e))