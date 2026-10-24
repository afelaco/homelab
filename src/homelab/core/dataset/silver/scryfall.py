from polars import Float64, Int64, String

from homelab.core.dataset import Dataset

cards = Dataset(
    layer="silver",
    name="cards",
    schema={
        "card_id": String,
        "oracle_id": String,
        "card": String,
        "scryfall_url": String,
        "image_url": String,
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
