from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # fastapi
    secret_key: str = Field(...)
    algorithm: str = Field(...)
    access_token_expire_minutes: int = Field(30)
    password_reset_token_expire_minutes: int = Field(5)

    # DataBase
    database_url: str = Field(...)
    echo_sql: bool = Field(True)

    # SMTP
    smtp_server: str = Field(...)
    smtp_port: int = Field(...)
    sender_email: str = Field(...)
    reset_callback_url: str = Field(...)

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
