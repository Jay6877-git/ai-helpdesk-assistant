import os
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentResponse

UPLOAD_DIR = "uploads"

class DocumentService:
    def upload_document(self, file: UploadFile, uploaded_by: int, db: Session) -> DocumentResponse:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_extension = os.path.splitext(file.filename)[1]
        stored_filename = f"{uuid.uuid4()}{file_extension}"
        storage_key = os.path.join(UPLOAD_DIR, stored_filename)

        with open(storage_key, "wb") as buffer:
            buffer.write(file.file.read())

        document = Document(
            original_filename=file.filename,
            storage_provider = "local",
            storage_key = storage_key,
            uploaded_by = uploaded_by,
            content_type = file.content_type
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return DocumentResponse(
            id=document.id,
            original_filename=document.original_filename,
            storage_provider = document.storage_provider,
            storage_key = document.storage_key,
            uploaded_by = document.uploaded_by,
            content_type = document.content_type,
            created_at=document.created_at,
        )

document_service = DocumentService()