import homelab.core.dataset.silver.steam_store
import homelab.core.table.dimension
import polars as pl

from homelab.core.table import Table
from homelab.load import Load


class LoadDimCards(Load):
    @property
    def table(self) -> Table:
        return homelab.core.table.dimension.dim_app_details

    def run(self) -> None:
        self.table.replace_table(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        return self.get_app_details().unique("app_id").sort("app_id").select(self.table.model.columns.keys())

    @staticmethod
    def get_app_details() -> pl.DataFrame:
        return homelab.core.dataset.silver.steam_store.app_details.read_parquet()


if __name__ == "__main__":
    LoadDimCards().run()
