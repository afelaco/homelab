import polars as pl
import requests

import homelab.core.dataset.bronze.scryfall
import homelab.core.endpoint.scryfall
from homelab.extract.scryfall import ExtractScryfall


class ExtractScryfallOracleTags(ExtractScryfall):
    def __init__(self) -> None:
        super().__init__(
            endpoint=homelab.core.endpoint.scryfall.oracle_tags,
            dataset=homelab.core.dataset.bronze.scryfall.oracle_tags,
        )

    def get_data(self) -> pl.DataFrame:
        metadata = self.api_client.get(endpoint=self.endpoint)
        download_uri = metadata[0]["jsonl_download_uri"]

        path = self.dataset.path
        response = requests.get(download_uri, stream=True)
        response.raise_for_status()

        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return pl.read_ndjson(path)


if __name__ == "__main__":
    ExtractScryfallOracleTags().run()
