from fastapi import(
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session
from database.postgres import get_db
from services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# --------------------------------------------------
# Upload the Document
# --------------------------------------------------

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and proces the document.
    """
    #Temporary user ID
    #Authentication will provide the real user ID later.
    user_id = 1

    try:
        result = await DocumentService.upload_document(
            db=db,
            file=file,
            user_id=user_id
        )
        return result

    except HTTPException:
        raise 

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}"
        )

    # --------------------------------------------------
    # Get All the uploaded Documents
    # -------------------------------------------------

@router.get("/")
def get_all_documents(
    db: Session = Depends(get_db)
):
    """
    Get all uploaded documents.
    """
    from database.models import Document

    documents = (
        db.query(Document)
        .all()
    )
    return documents

# --------------------------------------------------
# Get all the Document By ID
# --------------------------------------------------

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a document by its ID.
    """

    from database.models import Document
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Document not found."
        )
    return document

# --------------------------------------------------
# Delete all the Document
# --------------------------------------------------

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete the whole document and also its stored vectors also
    """

    from database.models import Document
    from utils.file_utils import delete_uploaded_file
    from AI.vectorstore import VectorStore

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:

        raise HTTPException(
            status_code=status.HTTP_400_NOT_FOUND,
            detail="Document not found."
        )

    try:
        #Deletevectors from Qdrant
        VectorStore.delete_document(
            document.id
        )

        #Delete physical file
        delete_uploaded_file(
            document.file_path
        )

        #Delete PostgreSql record
        db.delete(document)
        db.commit()

        return{
            "message": "Document deleted successfully.",
            "document_id": document_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete docuemnt: {str(e)}"
        )