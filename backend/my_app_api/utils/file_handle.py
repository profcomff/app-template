# from msilib.schema import File
from fastapi import HTTPException
import aiofiles
import os

PATH = "pictures/"
FILE_NUMBER = 0


async def safe_file(file):
    if file is None:
        return 'uploads/no_pic.png'

    if not file.filename.split('.')[0] or not file.filename.lower().endswith('.png'):
        raise HTTPException(
            status_code=400, detail="Непраильное название, либо можно только расширение .png")

    file_path = os.path.join("uploads", file.filename)

    if os.path.exists(file_path):
        dir_files = os.listdir('uploads')
        file_path += str(sum([file.filename in dir_file for dir_file in dir_files]))

    async with aiofiles.open(file_path, "wb") as buffer:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            await buffer.write(chunk)

    return file_path
