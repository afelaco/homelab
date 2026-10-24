import polars as pl

import homelab.core.dataset.bronze.scryfall
import homelab.core.dataset.silver.scryfall
from homelab.transform import Transform


class TransformScryfallCards(Transform):
    def __init__(self) -> None:
        super().__init__(
            bronze_dataset=homelab.core.dataset.bronze.scryfall.cards,
            silver_dataset=homelab.core.dataset.silver.scryfall.cards,
            mapping={
                "id": "card_id",
                "name": "card",
                "scryfall_uri": "scryfall_url",
                "type_line": "type",
                "color_identity": "color",
            },
        )

    def get_data(self) -> pl.DataFrame:
        return (
            self.bronze_dataset.read_parquet()
            .rename(self.mapping)
            .with_columns(pl.col("color").list.join(separator=""))
            .with_columns(pl.col(pl.String).replace("", None))
            .unnest("image_uris")
            .rename({"normal": "image_url"})
            .unnest("prices")
            .rename({"eur": "price"})
        )


if __name__ == "__main__":
    TransformScryfallCards().run()
