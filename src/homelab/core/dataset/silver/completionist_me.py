from pandera.polars import Column, DataFrameSchema

from homeauto.core.dataset.silver import SilverDataset

steam_app = SilverDataset(
    container="completionist-me",
    name="steam-app",
    schema=DataFrameSchema(
        columns={
            "app_id": Column(str, unique=True),
            "completion_time": Column(int),
        },
        strict=True,
    ),
)
