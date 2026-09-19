from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.api.routes.auth import router as auth_router
from app.api.routes.districts import router as district_router
from app.api.routes.comapnies import router as comapny_router

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
app.include_router(
    auth_router,
    prefix=settings.api_v1_prefix
)
app.include_router(
    district_router,
    prefix=settings.api_v1_prefix
)
app.include_router(
    comapny_router,
    prefix=settings.api_v1_prefix
)
@app.get("/", tags=["system"])
def root():
    return {"message":"working fking fine"}
