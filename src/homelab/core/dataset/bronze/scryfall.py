from polars import Float64, List, String, Struct

from homelab.core.dataset import Dataset

cards = Dataset(
    layer="bronze",
    name="cards",
    schema={
        "id": String,
        "oracle_id": String,
        "name": String,
        "mana_cost": String,
        "cmc": Float64,
        "type_line": String,
        "oracle_text": String,
        "power": String,
        "toughness": String,
        "color_identity": List(String),
        "rarity": String,
        "prices": Struct(
            {
                "eur": Float64,
            }
        ),
    },
)

oracle_tags = Dataset(
    layer="bronze",
    name="oracle_tags",
    schema={
        "id": String,
        "slug": String,
        "description": String,
        "parent_ids": List(String),
        # "child_ids": List(String),
        "taggings": List(
            Struct(
                {
                    "oracle_id": String,
                    "weight": String,
                }
            )
        ),
    },
)
