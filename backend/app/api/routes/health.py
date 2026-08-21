from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health_check():
    return {
        "status": "running",
        "project": "Sentinel AI",
        "version": "0.1.0"
    }