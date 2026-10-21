from abc import ABC
from dataclasses import dataclass

import polars as pl
from pandera.polars import DataFrameSchema

from homeauto.core import get_logger
from homeauto.core.infra import Database, infra

logger = get_logger(name=__name__)


@dataclass
class Table(ABC):
    name: str
    schema: DataFrameSchema
    database: Database

    def replace_table(self, df: pl.DataFrame) -> None:
        df.pipe(self.schema.validate).write_database(
            table_name=self.name,
            connection=self.database.get_connection_string(keyvault=infra.keyvault),
            if_table_exists="replace",
        )

        logger.info("%s records written to %s", len(df), self.name)
