from pandera import Field
from polars import Float64, List, String, Struct

from homelab.core.model import Model


class CardsBronzeModel(Model):
    id: String = Field(unique=True)
    oracle_id: String
    name: String
    mana_cost: String | None = Field(nullable=True)
    cmc: Float64
    type_line: String
    oracle_text: String | None = Field(nullable=True)
    power: String | None = Field(nullable=True)
    toughness: String | None = Field(nullable=True)
    colors: List(String) | None = Field(nullable=True)
    color_identity: List(String)
    keywords: List(String)
    set: String
    set_name: String
    rarity: String
    prices: String | None = Field(nullable=True)

class OracleTagsBronzeModel(Model):
    object: String
    id: String | None = Field(unique=True)
    label: String
    slug: String
    type: String
    uri: String
    description: String | None = Field(nullable=True)
    parent_ids: List(String) | None = Field(nullable=True)
    child_ids: List(String) | None = Field(nullable=True)
    aliases: List(String) | None = Field(nullable=True)
    taggings: List(
        Struct(
            {
                "oracle_id": String,
                "weight": String,
                "annotation": String,
            }
        )
    )
