# import homeauto.core.dataset.bronze.steam_web
# import homeauto.core.dataset.silver.steam_web
# import polars as pl
# from homeauto.core.dataset.bronze import BronzeDataset
# from homeauto.core.dataset.silver import SilverDataset
# from homeauto.transform import Transform
#
#
# class TransformSteamWebOwnedGames(Transform):
#     @property
#     def input_dataset(self) -> BronzeDataset:
#         return homeauto.core.dataset.bronze.steam_web.owned_games
#
#     @property
#     def output_dataset(self) -> SilverDataset:
#         return homeauto.core.dataset.silver.steam_web.owned_games
#
#     @property
#     def mapping(self) -> dict[str, str]:
#         return {
#             "appid": "app_id",
#             "playtime_forever": "playtime",
#         }
#
#     def run(self) -> None:
#         self.output_dataset.write_parquet(df=self.get_data())
#
#     def get_data(self) -> pl.DataFrame:
#         return (
#             self.input_dataset.read_parquet()
#             .rename(self.mapping)
#             .with_columns(
#                 pl.col("app_id").cast(pl.String),
#                 pl.col("playtime").truediv(60).cast(pl.Int64),
#             )
#             .select(self.output_dataset.model.columns.keys())
#         )
#
#
# if __name__ == "__main__":
#     TransformSteamWebOwnedGames().run()
