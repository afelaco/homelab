# import homeauto.core.dataset.silver.completionist_me
# import homeauto.core.dataset.silver.steam_store
# import homeauto.core.dataset.silver.steam_web
# import homeauto.core.table.fact
# import polars as pl
# from homeauto.core.table.fact import FactTable
# from homeauto.load import Load
#
#
# class LoadFactAppDetails(Load):
#     @property
#     def table(self) -> FactTable:
#         return homeauto.core.table.fact.fact_app_details
#
#     def run(self) -> None:
#         self.table.replace_table(df=self.get_data())
#
#     def get_data(self) -> pl.DataFrame:
#         return (
#             self.get_app_details()
#             .filter(
#                 ~pl.all_horizontal(
#                     pl.col(
#                         [
#                             "developer",
#                             "publisher",
#                             "genre_id",
#                             "category_id",
#                         ]
#                     ).is_null()
#                 )
#             )
#             .unique(
#                 [
#                     "app_id",
#                     "developer",
#                     "publisher",
#                     "genre_id",
#                     "category_id",
#                 ]
#             )
#             .sort("app_id")
#             .select(self.table.model.columns.keys())
#         )
#
#     @staticmethod
#     def get_app_details() -> pl.DataFrame:
#         return homeauto.core.dataset.silver.steam_store.app_details.read_parquet()
#
#
# if __name__ == "__main__":
#     LoadFactAppDetails().run()
