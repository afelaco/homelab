from pandera.polars import Column, DataFrameSchema

from homeauto.core.dataset.gold import GoldDataset

dim_owned_games = GoldDataset(
    container="steam",
    name="dim-owned-games",
    schema=DataFrameSchema(
        columns={
            "id": Column(str, unique=True),
            "name": Column(str),
            "playtime": Column(int),
        },
        strict=True,
    ),
)
fact_owned_games_tags = GoldDataset(
    container="steam",
    name="fact-owned-games-tags",
    schema=DataFrameSchema(
        columns={
            "id": Column(str),
            "tag": Column(str),
        },
        strict=True,
    ),
)
