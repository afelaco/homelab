from homelab.core.api.response_model.scryfall.cards import (
    ScryfallCardsApiResponseModel,
)
from homelab.core.api.response_model.scryfall.oracle_tags import ScryfallOracleTagsApiResponseModel
from homelab.core.endpoint import Endpoint

cards = Endpoint(
    url="cards/search",
    model=ScryfallCardsApiResponseModel,
)
oracle_tags = Endpoint(
    url="bulk-data/oracle_tags",
    model=ScryfallOracleTagsApiResponseModel,
)
