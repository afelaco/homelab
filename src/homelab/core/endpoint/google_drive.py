from homelab.core.endpoint import Endpoint
from homelab.core.model.response.scryfall.cards import (
    CardsScryfallResponseModel,
)
from homelab.core.model.response.scryfall.oracle_tags import OracleTagsScryfallResponseModel

files = Endpoint(
    url="files",
    model=CardsScryfallResponseModel,
)
