from abc import ABC, abstractmethod

import polars as pl

from homelab.core.api.client import ApiClient
from homelab.core.dataset import Dataset
from homelab.core.endpoint import Endpoint


class Extract(ABC):
    def __init__(
        self,
        api_client: ApiClient,
        endpoint: Endpoint,
        dataset: Dataset,
    ) -> None:
        self.api_client = api_client
        self.endpoint = endpoint
        self.dataset = dataset

    def run(self) -> None:
        self.dataset.write_parquet(df=self.get_data())

    @abstractmethod
    def get_data(self) -> pl.DataFrame:
        pass
