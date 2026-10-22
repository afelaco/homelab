# import homeauto.core.dataset.silver.completionist_me
# import homeauto.core.dataset.silver.steam_store
# import homeauto.core.dataset.silver.steam_web
# import homeauto.core.table.dimension
# import polars as pl
# from homeauto.core.table.dimension import DimensionTable
# from homeauto.load import Load
#
#
# class LoadDimOwnedGames(Load):
#     @property
#     def table(self) -> DimensionTable:
#         return homeauto.core.table.dimension.dim_owned_games
#
#     def run(self) -> None:
#         self.table.replace_table(df=self.get_data())
#
#     def get_data(self) -> pl.DataFrame:
#         return self.get_owned_games().unique("app_id").sort("app_id").select(self.table.model.columns.keys())
#
#     @staticmethod
#     def get_owned_games() -> pl.DataFrame:
#         return homeauto.core.dataset.silver.steam_web.owned_games.read_parquet()
#
#
# if __name__ == "__main__":
#     LoadDimOwnedGames().run()
