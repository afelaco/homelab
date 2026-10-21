from pydantic import BaseModel, Field, model_serializer


class Achievement(BaseModel):
    api_name: str = Field(alias="apiname")
    achieved: int
    unlock_time: int = Field(alias="unlocktime")


class PlayerStats(BaseModel):
    steam_id: str = Field(alias="steamID")
    game_name: str = Field(alias="gameName")
    achievements: list[Achievement]


class SteamWebPlayerAchievementsApiResponseModel(BaseModel):
    player_stats: PlayerStats = Field(alias="playerstats")

    @model_serializer
    def serialize(self) -> PlayerStats:
        return self.player_stats
