from fastapi import APIRouter
from app.schemas.security_event import SecurityEvent

router = APIRouter(
    prefix="/events",
    tags=["Security Events"]
)


@router.post("/")
def create_security_event(event: SecurityEvent):
    return {
        "message": "Security event received",
        "event": event.model_dump()
    }