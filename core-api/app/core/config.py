from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Immigration Advisor - Core API"
    database_url: str = "postgresql+psycopg2://user:password@localhost:5432/immigration_advisor"
    internal_service_token: str = "dev-only-change-me"
    ml_service_url: str = "http://localhost:8100"
    cors_allowed_origins: str = "http://localhost:5173,http://localhost"

    @property
    def cors_allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"


settings = Settings()
