from abc import ABC

from pandera.polars import Column, DataFrameSchema
from polars import Boolean, Date, Float64, Int64, String

from homeauto.core.infra import Database
from homeauto.core.table import Table


class DimensionTable(Table, ABC):
    pass


dim_app_details = DimensionTable(
    name="dim_app_details",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(String),
            "short_description": Column(String),
            "about_the_game": Column(String),
            "detailed_description": Column(String),
            "metacritic": Column(Int64, nullable=True),
            "is_free": Column(Boolean),
            "initial_price": Column(Int64, nullable=True),
            "final_price": Column(Int64, nullable=True),
            "currency": Column(String, nullable=True),
            "discount_percent": Column(Int64, nullable=True),
            "release_date": Column(Date, nullable=True),
            "coming_soon": Column(Boolean),
        },
        strict=True,
    ),
    database=Database(),
)

dim_app_reviews = DimensionTable(
    name="dim_app_reviews",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(String, unique=True),
            "num_reviews": Column(Int64),
            "review_score": Column(Int64),
            "review_score_desc": Column(String),
            "total_positive": Column(Int64),
            "total_negative": Column(Int64),
            "total_reviews": Column(Int64),
            "total_score": Column(Float64, nullable=True),
        },
        strict=True,
    ),
    database=Database(),
)

dim_completion = DimensionTable(
    name="dim_completion",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(str, unique=True),
            "completion_time": Column(int),
        },
        strict=True,
    ),
    database=Database(),
)

dim_genre = DimensionTable(
    name="dim_genre",
    schema=DataFrameSchema(
        columns={
            "genre_id": Column(String, unique=True),
            "genre_description": Column(String),
        },
        strict=True,
    ),
    database=Database(),
)

dim_category = DimensionTable(
    name="dim_category",
    schema=DataFrameSchema(
        columns={
            "category_id": Column(String, unique=True),
            "category_description": Column(String),
        },
        strict=True,
    ),
    database=Database(),
)

dim_collection = DimensionTable(
    name="dim_collection",
    schema=DataFrameSchema(
        columns={
            "scryfall_id": Column(String, unique=True),
            "name": Column(String),
            "set": Column(String),
            "set_name": Column(String),
            "collector_number": Column(Int64),
            "released_at": Column(String),
            "layout": Column(String),
            "cmc": Column(Float64),
            "type_line": Column(String),
            "oracle_text": Column(String, nullable=True),
            "power": Column(String, nullable=True),
            "toughness": Column(String, nullable=True),
            "reserved": Column(Boolean),
            "game_changer": Column(Boolean),
            "oversized": Column(Boolean),
            "promo": Column(Boolean),
            "reprint": Column(Boolean),
            "variation": Column(Boolean),
            "rarity": Column(String),
            "full_art": Column(Boolean),
            "textless": Column(Boolean),
            "booster": Column(Boolean),
            "price": Column(String, nullable=True),
            "price_foil": Column(String, nullable=True),
            "collected": Column(Boolean),
            "foil": Column(Boolean, nullable=True),
        },
        strict=True,
    ),
    database=Database(),
)

dim_owned_games = DimensionTable(
    name="dim_owned_games",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(String, unique=True),
            "name": Column(String),
            "playtime": Column(Int64),
        },
        strict=True,
    ),
    database=Database(),
)
