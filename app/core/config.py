from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
    )

    APP_NAME: str = "AI Case Processing Service"
    APP_ENV: str = "development"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    # External platform simulation
    PLATFORM_FAILURE_RATE: float = 0.0  # 0.0 - 1.0
    PLATFORM_LATENCY_MIN_MS: int = 150
    PLATFORM_LATENCY_MAX_MS: int = 900
    PLATFORM_RETRY_MAX_ATTEMPTS: int = 3

    # External priority service (Mensajería)
    EXTERNAL_PRIORITY_BASE_URL: str = "http://localhost:8000"
    EXTERNAL_PRIORITY_TIMEOUT_S: float = 2.0

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )


settings = Settings()
