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
        paginated: bool = True,
    ) -> list[dict[str, Any]]:
        url = self.get_url(endpoint=endpoint)
        if paginated:
            has_more = True
            data: list[dict[str, Any]] = []
            while has_more:
                response = self.session.get(
                    url=url,
                    params=params,
                    headers={
                        "User-Agent": "homelab/1.0",
                        "accept": "application/json",
                    },
                )
                response.raise_for_status()
                sleep(1)  # Be kind to the Scryfall API
                page = endpoint.model.model_validate_json(response.content)
                url = page.next_page  # type: ignore
                has_more = page.has_more  # type: ignore
                data.extend(page.model_dump(by_alias=True))  # type: ignore

                logger.info("%s records read from %s", len(data), response.url)
        else:
            response = self.session.get(
                url=url,
                params=params,
                headers={
                    "User-Agent": "homelab/1.0",
                    "accept": "application/json",
                },
            )
            response.raise_for_status()
            data = endpoint.model.model_validate_json(response.content).model_dump(by_alias=True)  # type: ignore

            logger.info("%s records read from %s", len(data), response.url)

        return data
