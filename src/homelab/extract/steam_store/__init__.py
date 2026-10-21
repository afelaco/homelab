from abc import ABC

from homeauto.core.api.client.steam_store import SteamStoreApiClient
from homeauto.extract import Extract


class ExtractSteamStore(Extract, ABC):
    @property
    def api_client(self) -> SteamStoreApiClient:
        return SteamStoreApiClient()
