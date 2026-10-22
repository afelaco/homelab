from pydantic import BaseModel


class Endpoint:
    def __init__(self, url: str, model: type[BaseModel]) -> None:
        self.url = url
        self.model = model
