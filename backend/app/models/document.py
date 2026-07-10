from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from datetime import datetime, UTC

from app.db.database import Base

class Document(Base):
    """Uploaded source file plus the latest processing result for that file."""

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True
    )

    original_filename = Column(
        String,
        nullable=False
    )

    storage_provider = Column(
        String,
        nullable=False
    )

    storage_key = Column(
        String,
        nullable=False
    )

    # MIME type supplied by the upload client; extraction code can use this to
    # decide which parser is appropriate as more file types are supported.
    content_type = Column(
        String,
        nullable=False
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda : datetime.now(UTC),
        nullable=False
    )

    # Status and error fields let the API report long-running extraction state
    # without losing the original upload metadata.
    processing_status = Column(
        String,
        nullable=False,
        default='uploaded'
    )

    processing_error = Column(
        Text,
        nullable=True
    )

    # Full extracted text is kept on the document while normalized chunks live
    # in document_chunks for retrieval/search workflows.
    extracted_Text = Column(
        Text,
        nullable=True
    )
