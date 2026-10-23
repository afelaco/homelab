import polars as pl

import homelab.core.dataset.silver.scryfall
import homelab.core.table.dimension
from homelab.load import Load


class LoadDimCards(Load):
    def __init__(self) -> None:
        super().__init__(
            table=homelab.core.table.dimension.dim_cards,
        )

    def run(self) -> None:
        self.table.replace_table(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        return homelab.core.dataset.silver.scryfall.cards.read_parquet().sort("card").select(self.table.schema.keys())


if __name__ == "__main__":
    LoadDimCards().run()
