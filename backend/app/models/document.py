from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, UTC

from app.db.database import Base

class Document(Base):
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