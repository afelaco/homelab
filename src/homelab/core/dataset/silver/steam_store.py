from pandera.polars import Column, DataFrameSchema
from polars import Boolean, Date, Float64, Int64, String

from homeauto.core.dataset.silver import SilverDataset

app_details = SilverDataset(
    container="steam-store",
    name="app-details",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(String),
            "name": Column(String),
            "short_description": Column(String),
            "about_the_game": Column(String),
            "detailed_description": Column(String),
            "developer": Column(String, nullable=True),
            "publisher": Column(String, nullable=True),
            "genre_id": Column(String, nullable=True),
            "genre_description": Column(String, nullable=True),
            "category_id": Column(String, nullable=True),
            "category_description": Column(String, nullable=True),
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
)

app_reviews = SilverDataset(
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
            "total_score": Column(Float64, nullable=True),
        },
        strict=True,
    ),
)
