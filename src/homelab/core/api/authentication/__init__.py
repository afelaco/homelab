from abc import ABC, abstractmethod


class Authentication(ABC):
    @abstractmethod
    def get_auth_headers(self) -> dict[str, str]:
        pass
