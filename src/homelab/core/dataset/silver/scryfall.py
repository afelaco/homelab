from polars import Float64, String

from homelab.core.dataset import Dataset

cards = Dataset(
    layer="silver",
    name="cards",
    schema={
        "card_id": String,
        "oracle_id": String,
        "name": String,
        "mana_cost": String,
        "cmc": Float64,
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
        "tag_id": String,
        "slug": String,
        "description": String,
        "oracle_id": String,
        "weight": String,
    },
)
