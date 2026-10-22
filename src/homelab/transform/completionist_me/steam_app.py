# import homeauto.core.dataset.bronze.completionist_me
# import homeauto.core.dataset.silver.completionist_me
# import polars as pl
# from homeauto.core.dataset.bronze import BronzeDataset
# from homeauto.core.dataset.silver import SilverDataset
# from homeauto.transform import Transform
#
#
# class TransformCompletionistMeSteamApp(Transform):
#     @property
#     def input_dataset(self) -> BronzeDataset:
#         return homeauto.core.dataset.bronze.completionist_me.steam_app
#
#     @property
#     def output_dataset(self) -> SilverDataset:
#         return homeauto.core.dataset.silver.completionist_me.steam_app
#
#     @property
#     def mapping(self) -> dict[str, str]:
#         return {"completion_playtime_avg": "completion_time"}
#
#     def run(self) -> None:
#         self.output_dataset.write_parquet(df=self.get_data())
#
#     def get_data(self) -> pl.DataFrame:
#         return (
#             self.input_dataset.read_parquet()
#             .rename(mapping=self.mapping)
#             .with_columns(pl.col("completion_time").str.extract(r"(\d+)h").cast(pl.Int64))
#             .filter(pl.col("completion_time").is_not_null())
#             .select(self.output_dataset.model.columns.keys())
#         )
#
#
# if __name__ == "__main__":
#     TransformCompletionistMeSteamApp().run()
