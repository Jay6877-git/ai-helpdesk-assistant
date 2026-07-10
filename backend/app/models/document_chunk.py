from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, UTC

from app.db.database import Base

class DocumentChunk(Base):
    """Searchable text segment extracted from an uploaded document."""

    __tablename__ = 'document_chunks'

    id = Column(
        Integer,
        primary_key=True
    )

    document_id = Column(
        Integer,
        ForeignKey('documents.id'),
        nullable=False
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    # Page number is 1-based so API/debug output lines up with PDF viewers.
    page_number = Column(
        Integer,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
    )
