from abc import ABC, abstractmethod
from typing import Any

import requests

from homelab.core.endpoint import Endpoint


class ApiClient(ABC):
    def __init__(self, base_url: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.base_url = base_url
        self.session = requests.Session()

    @abstractmethod
    def get_url(self, endpoint: Endpoint) -> str:
        pass

    @abstractmethod
    def get(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]] | dict[str, Any]:
        pass
