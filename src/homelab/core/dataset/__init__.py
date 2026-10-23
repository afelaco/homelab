from pathlib import Path
from typing import Literal

import polars as pl
from polars import List, Struct
from polars.datatypes import DataTypeClass

from homelab import SETTINGS
from homelab.core import get_logger

logger = get_logger(name=__name__)


class Dataset:
    def __init__(
        self,
        name: str,
        schema: dict[str, DataTypeClass | List | Struct],
        layer: Literal["bronze", "silver", "gold"],
    ):
        self.name = name
        self.schema = schema
        self.layer = layer
        self.path = self.get_path()

    def get_path(self) -> Path:
        return Path(f"{SETTINGS.ROOT}/data/{self.layer}/{self.name}.parquet").resolve()

    def read_parquet(self) -> pl.DataFrame:
        df = pl.read_parquet(source=self.path).pipe(self.validate)

        logger.info("%s records read from %s", len(df), self.path)

        return df

    def write_parquet(self, df: pl.DataFrame) -> None:
        df.pipe(self.validate).write_parquet(file=self.path)

        logger.info("%s records written to %s", len(df), self.path)

    def validate(self, df: pl.DataFrame) -> pl.DataFrame:
        return df.select(self.schema.keys())
