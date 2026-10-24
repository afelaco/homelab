import polars as pl

import homelab.core.dataset.silver.scryfall
import homelab.core.table.fact
from homelab.load import Load


class LoadFactCardsTags(Load):
    def __init__(self) -> None:
        super().__init__(
            table=homelab.core.table.fact.fact_cards_tags,
        )

    def run(self) -> None:
        self.table.replace_table(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        return (
            homelab.core.dataset.silver.scryfall.oracle_tags.read_parquet()
            .sort("oracle_id")
            .select(self.table.schema.keys())
        )


if __name__ == "__main__":
    LoadFactCardsTags().run()
