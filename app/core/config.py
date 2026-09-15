from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SkillSync"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/kaushallens"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False

    # Security & JWT
    SECRET_KEY: str = "development_secret_key_change_in_production"
    ALGORITHM: str = Field(default="HS256", alias="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, alias="JWT_ACCESS_TOKEN")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, alias="JWT_REFRESH_TOKEN")

    # Application Host
    BASE_URL: str = "http://localhost:8000"

    @property
    def api_v1_prefix(self) -> str:
        return self.API_V1_PREFIX

    @property
    def sync_database_url(self) -> str:
        """Ensure psycopg v3 driver prefix is used with SQLAlchemy 2.0."""
        url = self.DATABASE_URL.strip()
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

