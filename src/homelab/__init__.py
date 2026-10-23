from typing import Any

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ROOT: str = "/Users/admin/Repositories"
    GOOGLE_API_KEY: dict[str, Any] = {}

    model_config = SettingsConfigDict(env_file=find_dotenv())


SETTINGS = Settings()
