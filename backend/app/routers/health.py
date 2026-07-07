from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """Return a lightweight status response for uptime checks."""
    return {"status": "ok"}
