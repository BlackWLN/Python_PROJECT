import secrets
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Quiz API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database - provide via environment / .env, no secrets committed to git
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "questiondb"
    POSTGRES_PORT: str = "5432"

    # Some managed Postgres providers (Render, Neon, Supabase, Railway) expose
    # a single connection string instead of separate host/user/password.
    DATABASE_URL: Union[str, None] = None

    # Auth. Falls back to a random per-process key if not set, so the app
    # never silently runs with a known default secret. Set SECRET_KEY
    # explicitly in production so tokens survive restarts/deploys.
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Comma separated list of allowed origins, e.g.
    # "https://myapp.streamlit.app,http://localhost:8501"
    BACKEND_CORS_ORIGINS: Union[List[str], str] = "*"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and v != "*":
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()