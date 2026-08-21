from app.schemas.security_event import SecurityEvent
from app.services.risk_engine import calculate_risk


def process_security_event(event: SecurityEvent) -> dict:
    risk = calculate_risk(event)

    return {
        "status": "processed",
        "event": event.model_dump(),
        "risk": risk
    }