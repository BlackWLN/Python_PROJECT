from pydantic import BaseSettings


class Settings(BaseSettings):
    # Настройки БД
    DATABASE_URL: str

    class Config:
        env_file = "../.env"
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
