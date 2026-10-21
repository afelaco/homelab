from pandera.polars import Column, DataFrameSchema
from polars import Boolean, Float64, Int64, String

from homeauto.core.dataset.silver import SilverDataset

collection = SilverDataset(
    container="manabox",
    name="collection",
    schema=DataFrameSchema(
        columns={
            "scryfall_id": Column(String, unique=True),
            "name": Column(String),
            "set_code": Column(String),
            "set_name": Column(String),
            "collector_number": Column(Int64),
            "foil": Column(Boolean),
            "rarity": Column(String),
            "purchase_price": Column(Float64),
            "purchase_price_currency": Column(String),
        },
        strict=True,
    ),
)
