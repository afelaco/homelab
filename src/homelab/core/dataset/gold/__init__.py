from dataclasses import dataclass

from homeauto.core.dataset import Dataset
from homeauto.core.infra import StorageAccount, infra


@dataclass
class GoldDataset(Dataset):
    storage_account: StorageAccount = infra.datalake.gold

    def get_path(self) -> str:
        return f"abfss://{self.container}/{self.name}.parquet"
