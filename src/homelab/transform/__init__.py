from abc import ABC, abstractmethod

import polars as pl

from homelab.core.dataset import Dataset


class Transform(ABC):
    def __init__(
        self,
        bronze_dataset: Dataset,
        silver_dataset: Dataset,
        mapping= dict[str, str]
    ):
        self.bronze_dataset = bronze_dataset
        self.silver_dataset = silver_dataset
        self.mapping = mapping

    def run(self) -> None:
        self.silver_dataset.write_parquet(df=self.get_data())

    @abstractmethod
    def get_data(self) -> pl.DataFrame:
        pass
