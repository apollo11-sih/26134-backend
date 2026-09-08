from logging import DEBUG
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "SkillSync",
    DEBUG: bool = False,

    DATABASE_URL: str
    REDIS_URL: str

    SECRET_KEY: str
    ALGORITHM: str = Field(alias="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(alias="JWT_ACCESS_TOKEN")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(alias="JWT_REFRESH_TOKEN")

    BASE_URL: str

    REDIS_ENABLED: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True
    )

settings = Settings()