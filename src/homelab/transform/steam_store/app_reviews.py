import homeauto.core.dataset.bronze.steam_store
import homeauto.core.dataset.silver.steam_store
import polars as pl
from homeauto.core.dataset.bronze import BronzeDataset
from homeauto.core.dataset.silver import SilverDataset
from homeauto.transform import Transform


class TransformSteamStoreAppReviews(Transform):
    @property
    def input_dataset(self) -> BronzeDataset:
        return homeauto.core.dataset.bronze.steam_store.app_reviews

    @property
    def output_dataset(self) -> SilverDataset:
        return homeauto.core.dataset.silver.steam_store.app_reviews

    @property
    def mapping(self) -> dict[str, str]:
        return {}

    def run(self) -> None:
        self.output_dataset.write_parquet(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        return (
            self.input_dataset.read_parquet()
            .with_columns(total_score=pl.col("total_positive").truediv("total_reviews"))
            .select(self.output_dataset.model.columns.keys())
        )


if __name__ == "__main__":
    TransformSteamStoreAppReviews().run()
