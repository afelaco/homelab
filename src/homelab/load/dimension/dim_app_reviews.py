# import homeauto.core.dataset.silver.completionist_me
# import homeauto.core.dataset.silver.steam_store
# import homeauto.core.dataset.silver.steam_web
# import homeauto.core.table.dimension
# import polars as pl
# from homeauto.core.table.dimension import DimensionTable
# from homeauto.load import Load
#
#
# class LoadDimAppReviews(Load):
#     @property
#     def table(self) -> DimensionTable:
#         return homeauto.core.table.dimension.dim_app_reviews
#
#     def run(self) -> None:
#         self.table.replace_table(df=self.get_data())
#
#     def get_data(self) -> pl.DataFrame:
#         return self.get_app_reviews().sort("app_id").select(self.table.model.columns.keys())
#
#     @staticmethod
#     def get_app_reviews() -> pl.DataFrame:
#         return homeauto.core.dataset.silver.steam_store.app_reviews.read_parquet()
#
#
# if __name__ == "__main__":
#     LoadDimAppReviews().run()
