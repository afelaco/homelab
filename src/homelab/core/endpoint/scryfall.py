from homelab.core.api.response_model.scryfall.cards import (
    ScryfallCardsApiResponseModel,
)
from homelab.core.endpoint import Endpoint

cards = Endpoint(
    url="cards/search",
    model=ScryfallCardsApiResponseModel,
)
