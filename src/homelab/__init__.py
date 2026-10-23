from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ROOT: str = "/Users/admin/Repositories"

    model_config = SettingsConfigDict(env_file=find_dotenv())


SETTINGS = Settings()
