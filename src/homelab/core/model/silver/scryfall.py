import pandera.polars as pa

from homelab.core.model import Model


class CardsSilverModel(Model):
    id: str = pa.Field(unique=True)
    oracle_id: str
    name: str
    mana_cost: str = pa.Field(nullable=True)
    cmc: float
    type_line: str
    oracle_text: str = pa.Field(nullable=True)
    power: str = pa.Field(nullable=True)
    toughness: str = pa.Field(nullable=True)
    colors: str = pa.Field(nullable=True)
    color_identity: str
    keywords: str
    set: str
    set_name: str
    rarity: str
    prices: str = pa.Field(nullable=True)
