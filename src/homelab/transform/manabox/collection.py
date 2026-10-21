import homeauto.core.dataset.bronze.manabox
import homeauto.core.dataset.silver.manabox
import polars as pl
from homeauto.core.dataset.bronze import BronzeDataset
from homeauto.core.dataset.silver import SilverDataset
from homeauto.transform import Transform


class TransformManaBoxCollection(Transform):
    @property
    def input_dataset(self) -> BronzeDataset:
        return homeauto.core.dataset.bronze.manabox.collection

    @property
    def output_dataset(self) -> SilverDataset:
        return homeauto.core.dataset.silver.manabox.collection

    @property
    def mapping(self) -> dict[str, str]:
        return {
            "Name": "name",
            "Set code": "set_code",
            "Set name": "set_name",
            "Collector number": "collector_number",
            "Foil": "foil",
            "Rarity": "rarity",
            "Quantity": "quantity",
            "ManaBox ID": "manabox_id",
            "Scryfall ID": "scryfall_id",
            "Purchase price": "purchase_price",
            "Misprint": "misprint",
            "Altered": "altered",
            "Condition": "condition",
            "Language": "language",
            "Purchase price currency": "purchase_price_currency",
        }

    def run(self) -> None:
        self.output_dataset.write_parquet(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        return (
            self.input_dataset.read_parquet()
            .rename(self.mapping)
            .with_columns(foil=pl.col("foil").eq("foil"))
            .select(self.output_dataset.model.columns.keys())
        )


if __name__ == "__main__":
    TransformManaBoxCollection().run()
