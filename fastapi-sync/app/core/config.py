from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    database_url: str = Field(...)
    secret_key: str = Field(...)
    algorithm: str = Field(...)
    access_token_expire_minutes: int = Field(30)
    echo_sql: bool = Field(True)
    test: bool = Field(False)

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

# Access settings through the `settings` instance
# print(settings.database_url)
# print(settings.secret_key)
# print(settings.algorithm)
# print(settings.access_token_expire_minutes)
# print(settings.echo_sql)
# print(settings.test)
