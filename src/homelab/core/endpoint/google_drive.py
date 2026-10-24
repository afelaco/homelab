from homelab.core.endpoint import Endpoint
from homelab.core.model.response.scryfall.cards import (
    CardsScryfallResponseModel,
)

files = Endpoint(
    url="files",
    model=CardsScryfallResponseModel,
)
