import json
from pathlib import Path
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic import BaseModel

from homeauto.core import get_logger

logger = get_logger(name=__name__)


class KeyVault(BaseModel):
    uri: str

    def get_secret(self, secret_name: str) -> Any:
        credential = DefaultAzureCredential()
        client = SecretClient(
            vault_url=self.uri,
            credential=credential,
        )
        value = client.get_secret(secret_name).value

        logger.info("%s read from %s", secret_name, self.uri)

        return value


class Database:
    host = "192.168.0.105"
    port = "5432"
    secret_username = "POSTGRES-USER"
    secret_password = "POSTGRES-PASSWORD"

    def get_connection_string(self, keyvault: KeyVault) -> str:
        username = keyvault.get_secret(self.secret_username)
        password = keyvault.get_secret(self.secret_password)
        return f"postgresql+psycopg2://{username}:{password}@{self.host}:{self.port}/postgres"


class StorageAccount(BaseModel):
    name: str
    secret: str

    def get_storage_options(self, keyvault: KeyVault) -> dict[str, str]:
        return {
            "account_name": self.name,
            "account_key": keyvault.get_secret(self.secret),
        }


class DataLake(BaseModel):
    bronze: StorageAccount
    silver: StorageAccount
    gold: StorageAccount


class Infrastructure(BaseModel):
    datalake: DataLake
    keyvault: KeyVault


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"

with open(CONFIG_PATH) as f:
    infra_json = json.load(f)

infra = Infrastructure.model_validate(infra_json)
