from pandera.polars import Column, DataFrameSchema
from polars import Boolean, Int64, List, String, Struct

from homeauto.core.dataset.bronze import BronzeDataset

app_details = BronzeDataset(
    container="steam-store",
    name="app-details",
    schema=DataFrameSchema(
        columns={
            "steam_appid": Column(Int64, nullable=True),
            "name": Column(String, nullable=True),
            "short_description": Column(String, nullable=True),
            "about_the_game": Column(String, nullable=True),
            "detailed_description": Column(String, nullable=True),
            "developers": Column(List(String), nullable=True),
            "publishers": Column(List(String), nullable=True),
            "genres": Column(
                List(
                    Struct(
                        {
                            "id": String,
                            "description": String,
                        }
                    )
                ),
                nullable=True,
            ),
            "categories": Column(
                List(
                    Struct(
                        {
                            "id": Int64,
                            "description": String,
                        }
                    )
                ),
                nullable=True,
            ),
            "metacritic": Column(Int64, nullable=True),
            "is_free": Column(Boolean, nullable=True),
            "price_overview": Column(
                Struct(
                    {
                        "currency": String,
                        "initial": Int64,
                        "final": Int64,
                        "discount_percent": Int64,
                    }
                ),
                nullable=True,
            ),
            "release_date": Column(
                Struct(
                    {
                        "coming_soon": Boolean,
                        "date": String,
                    }
                ),
                nullable=True,
            ),
        },
        strict=True,
    ),
)


app_reviews = BronzeDataset(
    container="steam-store",
    name="app-reviews",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(String, unique=True),
            "num_reviews": Column(Int64),
            "review_score": Column(Int64),
            "review_score_desc": Column(String),
            "total_positive": Column(Int64),
            "total_negative": Column(Int64),
            "total_reviews": Column(Int64),
        },
        strict=True,
    ),
)
