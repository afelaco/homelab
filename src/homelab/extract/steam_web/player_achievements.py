import homeauto.core.dataset.bronze.steam_web
import homeauto.core.dataset.silver.steam_web
import homeauto.core.endpoint.steam_web
import polars as pl
from homeauto.core import get_logger
from homeauto.core.dataset.bronze import BronzeDataset
from homeauto.core.endpoint import Endpoint
from homeauto.extract.steam_web import ExtractSteamWeb

logger = get_logger(name=__name__)


class ExtractSteamWebPlayerAchievements(ExtractSteamWeb):
    @property
    def endpoint(self) -> Endpoint:
        return homeauto.core.endpoint.steam_web.ISteamUserStats.player_achievements

    @property
    def dataset(self) -> BronzeDataset:
        return homeauto.core.dataset.bronze.steam_web.player_achievements

    def run(self) -> None:
        self.dataset.write_parquet(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        played_games = self.get_owned_games().filter(pl.col("playtime").gt(0)).get_column("app_id")
        data = []
        for app_id in played_games[:3]:
            try:
                data.extend(
                    self.api_client.get(
                        endpoint=self.endpoint,
                        params={"appid": app_id},
                    )
                )
            except Exception as e:
                logger.error(e)
                continue
        return pl.DataFrame(data=data)

    @staticmethod
    def get_owned_games() -> pl.DataFrame:
        return homeauto.core.dataset.silver.steam_web.owned_games.read_parquet()


if __name__ == "__main__":
    data = ExtractSteamWebPlayerAchievements().get_data().to_pandas()
