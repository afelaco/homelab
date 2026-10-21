import polars as pl

import homelab.core.dataset.bronze.scryfall
import homelab.core.dataset.silver.scryfall
import homelab.core.endpoint.scryfall
from homelab.transform import Transform


class TransformScryfallCards(Transform):
    def __init__(self) -> None:
        super().__init__(
            bronze_dataset=homelab.core.dataset.bronze.scryfall.cards,
            silver_dataset=homelab.core.dataset.silver.scryfall.cards,
        )

    def get_data(self) -> pl.DataFrame:
        return self.bronze_dataset.read_parquet().explode("colors").explode("color_identity").explode("keywords")


if __name__ == "__main__":
    data = TransformScryfallCards().get_data().to_pandas()