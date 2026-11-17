from functools import lru_cache
from typing import Literal

from cryptography.fernet import Fernet
from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: Literal["development", "staging", "production", "test"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int = Field(default=20, ge=1, le=200)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, le=100)

    REDIS_URL: RedisDsn

    ENCRYPTION_KEY: str
    REQUIRE_HTTPS_ENDPOINTS: bool = True

    MAX_PAYLOAD_BYTES: int = Field(default=262_144, ge=1024, le=10_485_760)
    DEFAULT_MAX_ATTEMPTS: int = Field(default=5, ge=1, le=20)
    DEFAULT_RATE_LIMIT_PER_SEC: int = Field(default=10, ge=1, le=10_000)

    WORKER_BATCH_SIZE: int = Field(default=50, ge=1, le=500)
    WORKER_POLL_INTERVAL_SEC: float = Field(default=0.5, ge=0.05, le=30.0)
    SWEEPER_TIMEOUT_SEC: int = Field(default=60, ge=10, le=3600)

    CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = Field(default=5, ge=1, le=100)
    CIRCUIT_BREAKER_COOLDOWN_SEC: int = Field(default=30, ge=5, le=3600)

    @field_validator("ENCRYPTION_KEY")
    @classmethod
    def validate_fernet_key(cls, v: str) -> str:
        try:
            Fernet(v.encode("utf-8"))
        except Exception as exc:
            raise ValueError(
                "ENCRYPTION_KEY must be a valid 32-byte URL-safe base64-encoded Fernet key"
            ) from exc
        return v

@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]