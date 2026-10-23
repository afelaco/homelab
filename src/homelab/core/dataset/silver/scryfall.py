from polars import Float64, String, Int64

from homelab.core.dataset import Dataset

cards = Dataset(
    layer="silver",
    name="cards",
    schema={
        "card_id": String,
        "oracle_id": String,
        "card": String,
        "mana_cost": String,
        "cmc": Int64,
        "type": String,
        "oracle_text": String,
        "power": String,
        "toughness": String,
        "color": String,
        "rarity": String,
        "price": Float64,
    },
)

oracle_tags = Dataset(
    layer="silver",
    name="oracle_tags",
    schema={
        "oracle_id": String,
        "tag_id": String,
        "tag": String,
        "description": String,
        "weight": String,
    },
)
