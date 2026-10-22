from homelab.core.endpoint import Endpoint
from homelab.core.model.response.scryfall.cards import (
    CardsScryfallResponseModel,
)
from homelab.core.model.response.scryfall.oracle_tags import OracleTagsScryfallResponseModel

cards = Endpoint(
    url="cards/search",
    model=CardsScryfallResponseModel,
)
oracle_tags = Endpoint(
    url="bulk-data/oracle_tags",
    model=OracleTagsScryfallResponseModel,
)
