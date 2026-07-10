import os
import uuid
import fitz

from fastapi import UploadFile,HTTPException, status
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.document import DocumentResponse

UPLOAD_DIR = "uploads"

class DocumentService:
    """Business logic for storing files and extracting searchable text."""

    def upload_document(self, file: UploadFile, uploaded_by: int, db: Session) -> DocumentResponse:
        """Persist an uploaded file locally and create its document record."""
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Use a generated filename so different users can upload files with the
        # same original name without overwriting each other.
        file_extension = os.path.splitext(file.filename)[1]
        stored_filename = f"{uuid.uuid4()}{file_extension}"
        storage_key = os.path.join(UPLOAD_DIR, stored_filename)

        try:
            with open(storage_key, "wb") as buffer:
                buffer.write(file.file.read())
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Failed to save uploaded file.",
            )

        # The database keeps metadata and processing state; the binary file
        # itself stays in local storage referenced by storage_key.
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
            processing_status = document.processing_status,
            processing_error=document.processing_error,
        )

    def extract_text(self, document_id: int, user_id: int, db: Session) -> DocumentResponse:
        """Extract PDF text, rebuild document chunks, and update processing state."""
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.uploaded_by == user_id,
        ).first()

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )

        document.processing_status = "processing"
        db.commit()

        try:
            # Accumulate chunks in memory first so the old chunks are only
            # replaced after the PDF has been read successfully.
            page_texts = []
            chunk_index = 0
            new_chunks: list[DocumentChunk] = []

            with fitz.open(document.storage_key) as pdf:

                for page_index in range(len(pdf)):
                    page = pdf.load_page(page_index)
                    page_text = page.get_text()

                    page_texts.append(page_text)

                    page_chunks = self.chunk(page_text)

                    for chunk in page_chunks:
                        new_chunks.append(
                            DocumentChunk(
                                document_id=document.id,
                                chunk_index=chunk_index,
                                page_number=page_index + 1,
                                content=chunk,
                            )
                        )

                        chunk_index += 1


            full_text = "\n\n".join(page_texts)

            if not full_text:
                raise ValueError(
                    "No readable text was found in the document."
                )

            db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document.id,
            ).delete(synchronize_session=False)

            # Replace chunks as a set so chunk_index remains contiguous for the
            # latest extraction run.
            db.add_all(new_chunks)

            document.extracted_Text = full_text
            document.processing_status = "processed"
            document.processing_error = None

            db.commit()
            db.refresh(document)

        except Exception as error:

            # Roll back partial chunk writes and keep the document row available
            # with failure details for the caller.
            db.rollback()

            document.processing_status = "failed"
            document.processing_error = str(error)

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
            processing_status= document.processing_status,
            processing_error=document.processing_error,
        )

    def chunk(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Split text into overlapping windows for later retrieval/search."""
        if overlap >= chunk_size:
            raise ValueError(
                "Overlap must be smaller than chunk size."
            )

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            # Move back by `overlap` characters so context is preserved between
            # adjacent chunks.
            start = end - overlap

        return chunks

document_service = DocumentService()
