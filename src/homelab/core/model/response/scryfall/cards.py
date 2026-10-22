from pydantic import BaseModel

from homelab.core.model.response.scryfall import ScryfallResponseModel


class Prices(BaseModel):
    eur: str | None = None


class Data(BaseModel):
    id: str
    oracle_id: str
    name: str
    mana_cost: str | None = None
    cmc: float
    type_line: str
    oracle_text: str | None = None
    power: str | None = None
    toughness: str | None = None
    colors: list[str] | None = None
    color_identity: list[str]
    keywords: list[str]
    set: str
    set_name: str
    rarity: str
    prices: Prices


CardsScryfallResponseModel = ScryfallResponseModel[Data]
