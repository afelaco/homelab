from abc import ABC

from pandera.polars import Column, DataFrameSchema
from polars import String

from homeauto.core.infra import Database
from homeauto.core.table import Table


class FactTable(Table, ABC):
    pass


fact_app_details = FactTable(
    name="fact_app_details",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(String),
            "developer": Column(String, nullable=True),
            "publisher": Column(String, nullable=True),
            "genre_id": Column(String, nullable=True),
            "category_id": Column(String, nullable=True),
        },
        strict=True,
    ),
    database=Database(),
)
