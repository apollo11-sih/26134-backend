from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["system"])

@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        message="Backend service is healthy",
        version="0.0.1",
        developer="vedant"
        )
