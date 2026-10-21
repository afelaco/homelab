from pathlib import Path
from typing import Literal

import polars as pl
from pandera.polars import DataFrameModel

from homelab.core import get_logger

logger = get_logger(name=__name__)


class Dataset:
    def __init__(
        self,
        name: str,
        model: type[DataFrameModel],
        layer: Literal["bronze", "silver", "gold"],
    ):
        self.name = name
        self.model = model
        self.layer = layer
        self.path = self.get_path()

    def get_path(self) -> Path:
        return Path(f"/Users/alessandrofelaco/Repos/homelab/data/{self.layer}/{self.name}.parquet").resolve()

    def read_parquet(self) -> pl.DataFrame:
        df = pl.read_parquet(source=self.path).pipe(self.model.validate)

        logger.info("%s records read from %s", len(df), self.path)

        return df

    def write_parquet(self, df: pl.DataFrame) -> None:
        df.pipe(self.model.validate).write_parquet(file=self.path)

        logger.info("%s records written to %s", len(df), self.path)
