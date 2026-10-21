from typing import Dict

from pydantic import BaseModel, RootModel, model_serializer


class PriceOverview(BaseModel):
    currency: str
    initial: int
    final: int
    discount_percent: int


class Metacritic(BaseModel):
    score: int

    @model_serializer
    def serializer(self) -> int:
        return self.score


class Category(BaseModel):
    id: int
    description: str


class Genre(BaseModel):
    id: str
    description: str


class ReleaseDate(BaseModel):
    coming_soon: bool
    date: str


class Data(BaseModel):
    name: str
    steam_appid: int
    is_free: bool
    detailed_description: str
    about_the_game: str
    short_description: str
    developers: list[str] | None = None
    publishers: list[str] | None = None
    price_overview: PriceOverview | None = None
    metacritic: Metacritic | None = None
    categories: list[Category] | None = None
    genres: list[Genre] | None = None
    release_date: ReleaseDate


class Response(BaseModel):
    data: Data | None = None

    @model_serializer
    def serialize(self) -> Data | None:
        return self.data


class SteamStoreAppDetailsApiResponseModel(RootModel[Dict[str, Response]]):
    @property
    def app_id(self) -> Response:
        return next(iter(self.root.values()))

    @model_serializer
    def serialize(self) -> Response:
        return self.app_id
