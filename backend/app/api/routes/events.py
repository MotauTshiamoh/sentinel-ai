from fastapi import APIRouter
from app.schemas.security_event import SecurityEvent
from app.services.event_service import process_security_event

router = APIRouter(
    prefix="/events",
    tags=["Security Events"]
)


@router.post("/")
def create_security_event(event: SecurityEvent):
    return process_security_event(event)