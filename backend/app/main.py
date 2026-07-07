from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.db.database import Base, engine
from app.models.user import User

app = FastAPI(
    title="AI HelpDesk Assistant",
    description="Internal AI assistant for company employees",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(auth_router)