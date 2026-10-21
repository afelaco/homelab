import polars as pl
from tqdm import tqdm

import homeauto.core.dataset.bronze.steam_store
import homeauto.core.dataset.silver.steam_web
import homeauto.core.endpoint.steam_store
from homeauto.core import get_logger
from homeauto.core.dataset.bronze import BronzeDataset
from homeauto.core.endpoint import Endpoint
from homeauto.extract.steam_store import ExtractSteamStore

logger = get_logger(name=__name__)


class ExtractSteamStoreAppReviews(ExtractSteamStore):
    @property
    def endpoint(self) -> Endpoint:
        return homeauto.core.endpoint.steam_store.appreviews

    @property
    def dataset(self) -> BronzeDataset:
        return homeauto.core.dataset.bronze.steam_store.app_reviews

    def run(self) -> None:
        self.dataset.write_parquet(df=self.get_data())

    def get_data(self) -> pl.DataFrame:
        owned_games = self.get_owned_games().get_column("app_id")
        data = []
        for app_id in tqdm(owned_games):
            params = {"json": "1"}
            try:
                self.endpoint.url = f"appreviews/{app_id}"
                data.append(
                    {"app_id": app_id}
                    | self.api_client.get(
                        endpoint=self.endpoint,
                        params=params,
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
    ExtractSteamStoreAppReviews().run()
