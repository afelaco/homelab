from time import sleep
from typing import Any

from homeauto.core import get_logger
from homeauto.core.api.client import ApiClient
from homeauto.core.endpoint import Endpoint

logger = get_logger(name=__name__)


class SteamStoreApiClient(ApiClient):
    def __init__(self) -> None:
        super().__init__(base_url="https://store.steampowered.com")

    def get_url(self, endpoint: Endpoint) -> str:
        return f"{self.base_url}/{endpoint.url}"

    def get(self, endpoint: Endpoint, params: dict[str, str]) -> dict[str, Any]:
        params = params | {"json": "1"}
        response = self.session.get(
            url=self.get_url(endpoint=endpoint),
            params=params,
        )
        sleep(1)
        response.raise_for_status()
        data = endpoint.model.model_validate_json(response.content).model_dump(by_alias=True)

        return data
