from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.document import DocumentResponse
from app.schemas.user import UserResponse
from app.services.document_service import document_service
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/documents/upload", response_model=DocumentResponse)
def upload_document(
        file: UploadFile = File(...),
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """Store an uploaded document and attach it to the current user."""
    return document_service.upload_document(
        file = file,
        uploaded_by= current_user.id,
        db=db,
    )

@router.post("/documents/{document_id}/extract", response_model=DocumentResponse)
def extract_document(
        document_id: int,
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """Extract text for one of the current user's uploaded documents."""
    return document_service.extract_text(
        document_id = document_id,
        user_id=current_user.id,
        db=db,
    )

