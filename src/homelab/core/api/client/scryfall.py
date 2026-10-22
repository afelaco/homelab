from time import sleep
from typing import Any

from homelab.core import get_logger
from homelab.core.api.client import ApiClient
from homelab.core.endpoint import Endpoint

logger = get_logger(name=__name__)


class ScryfallApiClient(ApiClient):
    def __init__(self) -> None:
        super().__init__(base_url="https://api.scryfall.com")

    def get_url(self, endpoint: Endpoint) -> str:
        return f"{self.base_url}/{endpoint.url}"

    def get(
        self,
        endpoint: Endpoint,
        params: dict[str, str] | None = None,
    ) -> list[dict[str, Any]]:
        url: str | None = self.get_url(endpoint=endpoint)
        data: list[dict[str, Any]] = []
        while url:
            response = self.session.get(
                url=url,
                params=params,
                headers={
                    "User-Agent": "homelab/1.0",
                    "accept": "application/json",
                },
            )
            response.raise_for_status()
            page = endpoint.model.model_validate_json(response.content).model_dump()
            if page.get("data"):
                data.extend(page["data"])
            else:
                data.extend([page])

            logger.info("%s records read from %s", len(data), url)

            url = page.get("next_page") if page.get("next_page") else None
            sleep(1)

        return data
