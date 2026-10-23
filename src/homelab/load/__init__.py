from abc import ABC, abstractmethod

import polars as pl
from homelab.core.table import Table


class Load(ABC):
    def __init__(
        self,
        table: Table,
    ) -> None:
        self.table = table

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def get_data(self) -> pl.DataFrame:
        pass
