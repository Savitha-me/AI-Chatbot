from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status

from database.models import Document

from utils.file_utils import (
    allowed_file,
    generate_unique_filename,
    save_uploaded_file
)

class DocumentService:
    @staticmethod
    async def upload_document(
        db: Session,
        file: UploadFile,
        user_id: int
    ):
        """
        it uploads the document and stores the datas
        """

        #validates the file name
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is missing."
            )

        #validates the file type
        if not allowed_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format" 
            )

        #Generate unique filename
        stored_filename = generate_unique_filename(
            file.filename
        )

        #save file
        file_path=await save_uploaded_file(
            file,
            stored_filename
        )

        #store metadata
        document = Document(
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_type=file.content_type,
            file_size=file.size,
            file_path=file_path,
            uploaded_by=user_id,
            processing_status="uploaded"
        )

        db.add(document)

        db.commit()
        db.refresh(document)

        return{
            "message":"Document uploaded successfully.",
            "document_id":document.id,
            "filename":document.original_filename,
            "status":document.processing_status
        }