from datetime import datetime

from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    original_filename: str
    storage_provider: str
    storage_key: str
    content_type: str
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True