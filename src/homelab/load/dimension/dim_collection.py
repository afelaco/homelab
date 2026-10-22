# import homeauto.core.dataset.silver.manabox
# import homeauto.core.dataset.silver.scryfall
# import homeauto.core.table.dimension
# import polars as pl
# from homeauto.core.table.dimension import DimensionTable
# from homeauto.load import Load
#
#
# class LoadDimCollection(Load):
#     @property
#     def table(self) -> DimensionTable:
#         return homeauto.core.table.dimension.dim_collection
#
#     def run(self) -> None:
#         self.table.replace_table(df=self.get_data())
#
#     def get_data(self) -> pl.DataFrame:
#         cards = self.get_cards()
#         collection = self.get_collection()
#         return (
#             cards.join(
#                 other=collection,
#                 on="scryfall_id",
#                 how="left",
#             )
#             .with_columns(pl.col("collected").fill_null(False))
#             .sort("set", "collector_number")
#             .select(self.table.model.columns.keys())
#         )
#
#     @staticmethod
#     def get_cards() -> pl.DataFrame:
#         return homeauto.core.dataset.silver.scryfall.cards.read_parquet().select(
#             "scryfall_id",
#             "name",
#             "set",
#             "set_name",
#             "collector_number",
#             "released_at",
#             "layout",
#             "cmc",
#             "type_line",
#             "oracle_text",
#             "power",
#             "toughness",
#             "reserved",
#             "game_changer",
#             "oversized",
#             "promo",
#             "reprint",
#             "variation",
#             "rarity",
#             "full_art",
#             "textless",
#             "booster",
#             "price",
#             "price_foil",
#         )
#
#     @staticmethod
#     def get_collection() -> pl.DataFrame:
#         return (
#             homeauto.core.dataset.silver.manabox.collection.read_parquet()
#             .with_columns(collected=pl.lit(True))
#             .select(
#                 "scryfall_id",
#                 "collected",
#                 "foil",
#             )
#         )
#
#
# if __name__ == "__main__":
#     LoadDimCollection().run()
