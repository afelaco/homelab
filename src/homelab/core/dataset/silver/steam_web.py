from pandera.polars import Column, DataFrameSchema

from homeauto.core.dataset.silver import SilverDataset

owned_games = SilverDataset(
    container="steam-web",
    name="owned-games",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(str, unique=True),
            "name": Column(str),
            "playtime": Column(int),
        },
        strict=True,
    ),
)
