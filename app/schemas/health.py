from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    message: str | None = None
    version: str | None = None
    developer:str | None = None