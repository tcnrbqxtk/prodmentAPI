from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Prodment API"
    debug: bool = False

    # Database
    db_user: str
    db_password: str
    db_host: str = "db"  # имя сервиса в docker-compose
    db_port: int = 5432
    db_name: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # неделя

    # CORS
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "https://tcnrbqxtk.github.io",
    ]


settings = Settings()  # type: ignore[call-arg]
