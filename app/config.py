from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env from the project root, not the current working directory,
# so the app and pytest work no matter where they are launched from.
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    token_secret_key: str
    token_algorithm: str = "HS256"
    access_token_expire_hours: int = 24


settings = Settings()
