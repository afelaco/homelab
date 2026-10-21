import polars as pl

import homeauto.core.dataset.silver.completionist_me
import homeauto.core.dataset.silver.steam_store
import homeauto.core.dataset.silver.steam_web
import homeauto.core.table.dimension
from homeauto.core.table.dimension import DimensionTable
from homeauto.load import Load


class LoadDimGenre(Load):
    @property
    def table(self) -> DimensionTable:
        return homeauto.core.table.dimension.dim_genre

    def run(self) -> None:
        self.table.replace_table(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        return (
            self.get_app_details()
            .filter(pl.col("genre_id").is_not_null())
            .unique("genre_id")
            .sort("genre_id")
            .select(self.table.model.columns.keys())
        )

    @staticmethod
    def get_app_details() -> pl.DataFrame:
        return homeauto.core.dataset.silver.steam_store.app_details.read_parquet()


if __name__ == "__main__":
    LoadDimGenre().run()
