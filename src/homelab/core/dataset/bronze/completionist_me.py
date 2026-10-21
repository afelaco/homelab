from pandera.polars import Column, DataFrameSchema

from homeauto.core.dataset.bronze import BronzeDataset

steam_app = BronzeDataset(
    container="completionist-me",
    name="steam-app",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(str, unique=True),
            "completion_playtime_avg": Column(str, nullable=True),
        },
        strict=True,
    ),
)
