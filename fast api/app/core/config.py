from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    echo_sql: bool = Field(True, env="ECHO_SQL")
    test: bool = Field(False, env="TEST")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create an instance of Settings
settings = Settings()

# Access settings through the `settings` instance
print(settings.database_url)
print(settings.secret_key)
print(settings.algorithm)
print(settings.access_token_expire_minutes)
print(settings.echo_sql)
print(settings.test)
