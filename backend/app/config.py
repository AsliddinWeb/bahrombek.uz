from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    admin_username: str = "bahrombek"
    admin_password: str = "supersecret123"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 1 day
    database_url: str = "postgresql+asyncpg://user:pass@localhost/bahrombek_db"
    upload_dir: str = "./uploads"
    max_pdf_size_mb: int = 20
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
