from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    internal_service_token: str = "dev-only-change-me"

    class Config:
        env_file = ".env"


settings = Settings()
