from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.events import router as events_router

app = FastAPI(
    title="Sentinel AI",
    description="AI-powered cybersecurity intelligence platform",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(events_router)