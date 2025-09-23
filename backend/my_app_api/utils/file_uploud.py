import os
import uuid
import pandas as pd

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from my_app_api.models import FinesDataTemp, EvacuationsTemp, TrafficLightTemp, EvacuationRouteTemp,  Status
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
    allowed_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
    
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


async def process_fines_csv(file: UploadFile, db: Session, import_batch: uuid.UUID = None) -> dict:
    if not import_batch:
        import_batch = uuid.uuid4()
    
    filename = await save_uploaded_file(
        file,
        "csv_data",
        ['.csv']
    )
    
    file_path = os.path.join(settings.UPLOAD_DIR, "csv_data", filename)
    
    try:
        df = pd.read_csv(file_path)
        
        required_columns = ['date', 'violations_count', 'decrees_count', 'fines_imposed', 'fines_collected']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing_columns}")
        
        processed_count = 0
        for _, row in df.iterrows():
            date_obj = datetime.strptime(str(row['date']), '%Y-%m-%d').date()
            year = date_obj.year
            month = date_obj.month

            fine_temp = FinesDataTemp(
                date=date_obj,
                year=year,
                month=month,
                violations_count=row['violations_count'],
                decrees_count=row['decrees_count'],
                fines_imposed=float(row['fines_imposed']),
                fines_collected=float(row['fines_collected']),
                import_batch=import_batch,
                status=Status.PENDING
            )
            
            db.add(fine_temp)
            processed_count += 1
        
        db.commit()
        
        return {
            "import_batch": import_batch,
            "processed_records": processed_count,
            "filename": filename,
            "status": "success"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

async def process_evacuations_csv(file: UploadFile, db: Session, import_batch: uuid.UUID = None) -> dict:
    if not import_batch:
        import_batch = uuid.uuid4()
    
    filename = await save_uploaded_file(
        file,
        "csv_data",
        ['.csv']
    )
    
    file_path = os.path.join(settings.UPLOAD_DIR, "csv_data", filename)
    
    try:
        df = pd.read_csv(file_path)
        
        required_columns = ['date', 'tow_trucks_online', 'dispatches_count', 'evacuations_count', 'parking_receipts']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing_columns}")
        
        processed_count = 0
        for _, row in df.iterrows():
            date_obj = datetime.strptime(str(row['date']), '%Y-%m-%d').date()
            year = date_obj.year
            month = date_obj.month
            
            evacuation_temp = EvacuationsTemp(
                date=date_obj,
                year=year,
                month=month,
                tow_trucks_online=row['tow_trucks_online'],
                dispatches_count=row['dispatches_count'],
                evacuations_count=row['evacuations_count'],
                parking_receipts=float(row['parking_receipts']),
                import_batch=import_batch,
                status=Status.PENDING
            )
            
            db.add(evacuation_temp)
            processed_count += 1
        
        db.commit()
        
        return {
            "import_batch": import_batch,
            "processed_records": processed_count,
            "filename": filename,
            "status": "success"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

async def process_evacuation_routes_csv(file: UploadFile, db: Session, import_batch: uuid.UUID = None) -> dict:
    if not import_batch:
        import_batch = uuid.uuid4()
    
    filename = await save_uploaded_file(
        file,
        "csv_data",
        ['.csv']
    )
    
    file_path = os.path.join(settings.UPLOAD_DIR, "csv_data", filename)
    
    try:
        df = pd.read_csv(file_path)
        
        required_columns = ['year', 'month', 'route_description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing_columns}")
        
        processed_count = 0
        for _, row in df.iterrows():
            route_temp = EvacuationRouteTemp(
                year=int(row['year']),
                month=int(row['month']),
                route_description=row['route_description'],
                route_path=row.get('route_path', ''),
                import_batch=import_batch,
                status=Status.PENDING
            )
            
            db.add(route_temp)
            processed_count += 1
        
        db.commit()
        
        return {
            "import_batch": import_batch,
            "processed_records": processed_count,
            "filename": filename,
            "status": "success"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


async def process_traffic_lights_csv(file: UploadFile, db: Session, import_batch: uuid.UUID = None) -> dict:
    if not import_batch:
        import_batch = uuid.uuid4()
    
    filename = await save_uploaded_file(
        file,
        "csv_data",
        ['.csv']
    )
    
    file_path = os.path.join(settings.UPLOAD_DIR, "csv_data", filename)
    
    try:
        df = pd.read_csv(file_path)
        
        required_columns = ['address', 'light_type', 'installation_year']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing_columns}")
        
        processed_count = 0
        for _, row in df.iterrows():
            traffic_light_temp = TrafficLightTemp(
                address=row['address'],
                light_type=row['light_type'],
                installation_year=int(row['installation_year']),
                worked=row.get('worked', None),
                import_batch=import_batch,
                status=Status.PENDING
            )
            
            db.add(traffic_light_temp)
            processed_count += 1
        
        db.commit()
        
        return {
            "import_batch": import_batch,
            "processed_records": processed_count,
            "filename": filename,
            "status": "success"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


# Универсальная функция для определения типа CSV и выбора соответствующего обработчика
async def process_csv_file(file: UploadFile, db: Session, data_type: str = None) -> dict:
    """
    data_type: 'fines', 'evacuations', 'routes', 'traffic_lights'
    Если не указан, попытается определить автоматически
    """
    if data_type:
        processors = {
            'fines': process_fines_csv,
            'evacuations': process_evacuations_csv,
            'routes': process_evacuation_routes_csv,
            'traffic_lights': process_traffic_lights_csv
        }
        
        if data_type not in processors:
            raise HTTPException(status_code=400, detail="Invalid data type")
        
        return await processors[data_type](file, db)
    
    content = await file.read()
    await file.seek(0)
    

    temp_filename = await save_uploaded_file(file, "temp", ['.csv'])
    temp_path = os.path.join(settings.UPLOAD_DIR, "temp", temp_filename)
    
    try:
        df = pd.read_csv(temp_path)
        columns = set(df.columns)
        
        if {'date', 'violations_count', 'decrees_count'}.issubset(columns):
            return await process_fines_csv(file, db)
        elif {'date', 'tow_trucks_online', 'dispatches_count'}.issubset(columns):
            return await process_evacuations_csv(file, db)
        elif {'year', 'month', 'route_description'}.issubset(columns):
            return await process_evacuation_routes_csv(file, db)
        elif {'address', 'light_type', 'installation_year'}.issubset(columns):
            return await process_traffic_lights_csv(file, db)
        else:
            raise HTTPException(status_code=400, detail="Cannot determine data type from CSV columns")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)