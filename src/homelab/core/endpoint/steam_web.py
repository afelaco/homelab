from homeauto.core.api.response_model.steam_web.get_schema_for_game import (
    SteamWebGetSchemaForGameApiResponseModel,
)
from homeauto.core.api.response_model.steam_web.owned_games import (
    SteamWebOwnedGamesApiResponseModel,
)
from homeauto.core.api.response_model.steam_web.player_achievements import (
    SteamWebPlayerAchievementsApiResponseModel,
)
from homeauto.core.endpoint import Endpoint


class IPlayerService:
    __SERVICE = "IPlayerService"
    owned_games = Endpoint(
        url=f"{__SERVICE}/GetOwnedGames/v0001/",
        response_model=SteamWebOwnedGamesApiResponseModel,
    )


class ISteamUserStats:
    __SERVICE = "ISteamUserStats"
    get_schema_for_game = Endpoint(
        url=f"{__SERVICE}/GetSchemaForGame/v2/",
        response_model=SteamWebGetSchemaForGameApiResponseModel,
    )
    player_achievements = Endpoint(
        url=f"{__SERVICE}/GetPlayerAchievements/v0001/",
        response_model=SteamWebPlayerAchievementsApiResponseModel,
    )
