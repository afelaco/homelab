# import homeauto.core.dataset.bronze.steam_store
# import homeauto.core.dataset.silver.steam_store
# import polars as pl
# from homeauto.core.dataset.bronze import BronzeDataset
# from homeauto.core.dataset.silver import SilverDataset
# from homeauto.transform import Transform
#
#
# class TransformSteamStoreAppDetails(Transform):
#     @property
#     def input_dataset(self) -> BronzeDataset:
#         return homeauto.core.dataset.bronze.steam_store.app_details
#
#     @property
#     def output_dataset(self) -> SilverDataset:
#         return homeauto.core.dataset.silver.steam_store.app_details
#
#     @property
#     def mapping(self) -> dict[str, str]:
#         return {"steam_appid": "app_id"}
#
#     def run(self) -> None:
#         self.output_dataset.write_parquet(df=self.get_data())
#
#     def get_data(self) -> pl.DataFrame:
#         return (
#             self.input_dataset.read_parquet()
#             .rename(self.mapping)
#             .explode("developers")
#             .rename({"developers": "developer"})
#             .explode("publishers")
#             .rename({"publishers": "publisher"})
#             .explode("genres")
#             .unnest("genres")
#             .rename(
#                 {
#                     "id": "genre_id",
#                     "description": "genre_description",
#                 }
#             )
#             .explode("categories")
#             .unnest("categories")
#             .rename(
#                 {
#                     "id": "category_id",
#                     "description": "category_description",
#                 }
#             )
#             .unnest("price_overview")
#             .rename(
#                 {
#                     "initial": "initial_price",
#                     "final": "final_price",
#                 }
#             )
#             .unnest("release_date")
#             .rename({"date": "release_date"})
#             .filter(pl.col("app_id").is_not_null())
#             .with_columns(
#                 pl.col("app_id", "category_id").cast(pl.String),
#                 pl.col("release_date").str.strptime(pl.Date, format="%d %b, %Y", strict=False),
#             )
#             .select(self.output_dataset.model.columns.keys())
#         )
#
#
# if __name__ == "__main__":
#     TransformSteamStoreAppDetails().run()
