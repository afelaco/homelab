from pydantic import BaseModel

from homelab.core.model.response.scryfall import ScryfallResponseModel


class ImageUris(BaseModel):
    normal: str


class Prices(BaseModel):
    eur: str | None = None


class Data(BaseModel):
    id: str
    oracle_id: str
    name: str
    scryfall_uri: str | None
    image_uris: ImageUris | None = None
    mana_cost: str | None = None
    cmc: int
    type_line: str
    oracle_text: str | None = None
    power: str | None = None
    toughness: str | None = None
    color_identity: list[str]
    rarity: str
    prices: Prices


CardsScryfallResponseModel = ScryfallResponseModel[Data]
