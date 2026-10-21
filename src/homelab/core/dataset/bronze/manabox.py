from pandera.polars import Column, DataFrameSchema
from polars import Boolean, Float64, Int64, String

from homeauto.core.dataset.bronze import BronzeDataset

collection = BronzeDataset(
    container="manabox",
    name="collection",
    schema=DataFrameSchema(
        columns={
            "Name": Column(String),
            "Set code": Column(String),
            "Set name": Column(String),
            "Collector number": Column(Int64),
            "Foil": Column(String),
            "Rarity": Column(String),
            "Quantity": Column(Int64),
            "ManaBox ID": Column(Int64),
            "Scryfall ID": Column(String, unique=True),
            "Purchase price": Column(Float64),
            "Misprint": Column(Boolean),
            "Altered": Column(Boolean),
            "Condition": Column(String),
            "Language": Column(String),
            "Purchase price currency": Column(String),
        },
        strict=True,
    ),
)
