from abc import ABC

from homelab.core.api.client.google import GoogleApiClient
from homelab.core.api.client.scryfall import ScryfallApiClient
from homelab.core.dataset import Dataset
from homelab.core.endpoint import Endpoint
from homelab.extract import Extract


class ExtractGoogleDrive(Extract, ABC):
    def __init__(
        self,
        endpoint: Endpoint,
        dataset: Dataset,
    ):
        super().__init__(
            api_client=GoogleApiClient(),
            endpoint=endpoint,
            dataset=dataset,
        )
