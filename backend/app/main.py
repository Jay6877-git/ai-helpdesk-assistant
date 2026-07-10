from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.documents import router as document_router

from app.db.database import Base, engine

from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

# Import model modules before creating tables so SQLAlchemy registers them
# with Base.metadata.
app = FastAPI(
    title="AI HelpDesk Assistant",
    description="Internal AI assistant for company employees",
    version="0.1.0",
)

# Create database tables for the registered models at application startup.
Base.metadata.create_all(bind=engine)

# Register API route groups with the FastAPI application.
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(document_router)