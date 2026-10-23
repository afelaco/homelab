from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ROOT: str = "/Users/admin/Repositories"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "dummy"

    model_config = SettingsConfigDict(env_file=find_dotenv())


SETTINGS = Settings()
