from abc import ABC

from homeauto.core.api.client.steam_web import SteamWebApiClient
from homeauto.extract import Extract


class ExtractSteamWeb(Extract, ABC):
    @property
    def api_client(self) -> SteamWebApiClient:
        return SteamWebApiClient()
