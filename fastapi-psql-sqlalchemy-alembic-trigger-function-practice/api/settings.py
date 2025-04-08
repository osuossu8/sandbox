from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    DB_USER: str = Field(default="user")
    DB_PASSWORD: str = Field(default="password")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: str = Field(default="6543")
    DB_NAME: str = Field(default="sample_db")
