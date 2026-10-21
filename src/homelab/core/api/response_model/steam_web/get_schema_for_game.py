from pydantic import BaseModel, Field, model_serializer


class Achievement(BaseModel):
    name: str
    default_value: int = Field(alias="defaultValue")
    display_name: str = Field(alias="displayName")
    description: str


class AvailableGameStats(BaseModel):
    achievements: list[Achievement]

    @model_serializer
    def serialize(self) -> list[Achievement]:
        return self.achievements


class Game(BaseModel):
    game_name: str = Field(alias="gameName")
    game_version: str = Field(alias="gameVersion")
    available_game_stats: AvailableGameStats = Field(alias="availableGameStats")


class SteamWebGetSchemaForGameApiResponseModel(BaseModel):
    game: Game

    @model_serializer
    def serialize(self) -> Game:
        return self.game
