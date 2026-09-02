from fastapi import(
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database.postgres import get_db
from services.summary_service import SummaryService

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

@router.post("/{document_id}")
def generate_summary(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    it generates the short summary as a answer for the questions being asked by the user
    """
    try:
        result = SummaryService.generate_summary(
            db=db,
            document_id=document_id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate document summary."
        )