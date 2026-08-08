import os
import uuid
from pathlib import Path
import aiofiles
from fastapi import UploadFile

#folder where the uploaded files will be stored
UPLOAD_DIRECTORY="uploads"

#Allowed document formats
ALLOWED_EXTENSIONS={
    ".pdf",
    ".docx",
    ".txt"
}

def get_file_extension(filename: str) -> str:
    """
    returns the file extension from the document
    """
    return Path(filename).suffix.lower()

def allowed_file(filename: str) -> bool:
    """
    checks whether the uploaded file type is allowed
    """
    extension = get_file_extension(filename)
    return extension in ALLOWED_EXTENSIONS

def generate_unique_filename(filename: str) -> str:
    """
    generates the unique file name and store that file in the folder
    """
    unique_id = uuid.uuid4().hex
    return f"{unique_id}_{filename}"

async def save_uploaded_file(
        file: UploadFile,
        stored_filename: str
) -> str:
    """
    it saves the upload file by using the unique name created by ai
    """
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    file_path = os.path.join(
        UPLOAD_DIRECTORY,
        stored_filename
    )

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return file_path

def delete_uploaded_file(file_path: str) -> bool:
    """
    it deletes the file from the disk
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False