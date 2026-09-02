from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from database.models import Document
from AI.parser import DocumentParser
from AI.chunker import TextChunker
from AI.embedding import EmbeddingGenerator
from AI.vectorstore import VectorStore
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
            processing_status="processing"
        )

        db.add(document)

        db.commit()
        db.refresh(document)
        try:
            #extract the text from the document

            text = DocumentParser.extract_text(
                file_path
            )
            if not text.strip():
                raise ValueError(
                    "No text was recoginized in the document and could not extracted."
                )

            #chunk the text
            chunker = TextChunker()
            chunks = chunker.split_text(
                text
            )

            if not chunks:
                raise ValueError(
                    "No chunks were created from the document."
                )

            #generate the embeddings for the text extracted from the document
            embedding_generator = EmbeddingGenerator()
            embeddings = (
                embedding_generator.generator_embeddings(
                    chunks
                )
            )

            #create the qdrant collection
            VectorStore.create_collection()

            #store the vectors in qdrant
            VectorStore.store_embeddings(
                embeddings = embeddings,
                chunks = chunks,
                document_id = document.id,
                original_filename=file.filename
            )

            #update the processing status
            document.processing_status = "completed"
            db.commit()
            db.refresh(document)
            return{
              "message":"Document uploaded and processed successfully.",
              "document_id":document.id,
              "filename":document.original_filename,
              "status":document.processing_status,
              "chunks_created": len(chunks)
             }

        except Exception as e:

            #give the failed status or update the failed status
            document.processing_status = "failed"
            db.commit()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Document Processing failed: {str(e)}"
            )