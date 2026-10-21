import polars as pl

import homeauto.core.dataset.bronze.steam_web
import homeauto.core.endpoint.steam_web
from homeauto.core import get_logger
from homeauto.core.dataset.bronze import BronzeDataset
from homeauto.core.endpoint import Endpoint
from homeauto.extract.steam_web import ExtractSteamWeb

logger = get_logger(name=__name__)


class ExtractSteamWebOwnedGames(ExtractSteamWeb):
    @property
    def endpoint(self) -> Endpoint:
        return homeauto.core.endpoint.steam_web.IPlayerService.owned_games

    @property
    def dataset(self) -> BronzeDataset:
        return homeauto.core.dataset.bronze.steam_web.owned_games

    def run(self) -> None:
        self.dataset.write_parquet(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        params = {"include_appinfo": "true"}
        data = self.api_client.get(
            endpoint=self.endpoint,
            params=params,
        )
        return pl.DataFrame(data=data)


if __name__ == "__main__":
    ExtractSteamWebOwnedGames().run()
