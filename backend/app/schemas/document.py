from datetime import datetime

from pydantic import BaseModel

class DocumentResponse(BaseModel):
    """Public document metadata returned after upload or processing."""

    id: int
    original_filename: str
    storage_provider: str
    storage_key: str
    content_type: str
    uploaded_by: int
    created_at: datetime
    processing_status: str
    processing_error: str | None = None

    class Config:
        # Allows Pydantic to serialize SQLAlchemy model instances when needed.
        from_attributes = True
