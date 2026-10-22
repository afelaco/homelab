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
        "colors": List(String),
        "color_identity": List(String),
        "keywords": List(String),
        "set": String,
        "set_name": String,
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
    schema={},
)
