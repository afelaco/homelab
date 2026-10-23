from abc import ABC
from dataclasses import dataclass

import polars as pl
from polars.datatypes import DataTypeClass

from homelab.core import get_logger
from homelab.core.infrastructure import Database

logger = get_logger(name=__name__)


@dataclass
class Table(ABC):
    name: str
    schema: dict[str, DataTypeClass]
    database: Database

    def replace_table(self, df: pl.DataFrame) -> None:
        df.write_database(
            table_name=self.name,
            connection=self.database.get_connection_string(),
            if_table_exists="replace",
        )

        logger.info("%s records written to %s", len(df), self.name)
