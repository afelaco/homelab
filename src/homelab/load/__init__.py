from abc import ABC, abstractmethod

import polars as pl

from homeauto.core.table import Table


class Load(ABC):
    @property
    @abstractmethod
    def table(self) -> Table:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def get_data(self) -> pl.DataFrame:
        pass
