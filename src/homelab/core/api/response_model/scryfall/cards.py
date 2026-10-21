from pydantic import BaseModel, model_serializer

from homelab.core.api.response_model.scryfall import ScryfallApiResponseModel


class Prices(BaseModel):
    eur: str | None = None

    @model_serializer
    def model_serializer(self) -> str | None:
        return self.eur


class Card(BaseModel):
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


ScryfallCardsApiResponseModel = ScryfallApiResponseModel[Card]
