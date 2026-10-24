from abc import ABC

from homelab.core.infrastructure import DWH
from homelab.core.table import Table
from polars import String


class FactTable(Table):
    pass


fact_cards_tags = FactTable(
    name="fact_cards_tags",
    schema={
        "oracle_id": String,
        "tag_id": String,
    },
    database=DWH,
)

fact_synergies = FactTable(
    name="fact_synergies",
    schema={
        "tag_a": String,
        "tag_b": String,
    },
    database=DWH,
)


#
# fact_app_details = FactTable(
#     name="fact_app_details",
#     schema=DataFrameSchema(
#         columns={
#             "app_id": Column(String),
#             "developer": Column(String, nullable=True),
#             "publisher": Column(String, nullable=True),
#             "genre_id": Column(String, nullable=True),
#             "category_id": Column(String, nullable=True),
#         },
#         strict=True,
#     ),
#     database=Database(),
# )
