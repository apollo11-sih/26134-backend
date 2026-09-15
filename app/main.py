from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="skillsync",
    description="Labour Market Intelligence Platform",
    version="0.1.0",
)
app.include_router(
    health_router,
    prefix=settings.api_v1_prefix
)

@app.get("/", tags=["system"])
def root():
    return {
        "message": "Backend is running!!"
    }