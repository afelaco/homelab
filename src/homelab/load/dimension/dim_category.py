import homeauto.core.dataset.silver.completionist_me
import homeauto.core.dataset.silver.steam_store
import homeauto.core.dataset.silver.steam_web
import homeauto.core.table.dimension
import polars as pl
from homeauto.core.table.dimension import DimensionTable
from homeauto.load import Load


class LoadDimCategory(Load):
    @property
    def table(self) -> DimensionTable:
        return homeauto.core.table.dimension.dim_category

    def run(self) -> None:
        self.table.replace_table(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        return (
            self.get_app_details()
            .filter(pl.col("category_id").is_not_null())
            .unique("category_id")
            .sort("category_id")
            .select(self.table.model.columns.keys())
        )

    @staticmethod
    def get_app_details() -> pl.DataFrame:
        return homeauto.core.dataset.silver.steam_store.app_details.read_parquet()


if __name__ == "__main__":
    LoadDimCategory().run()
