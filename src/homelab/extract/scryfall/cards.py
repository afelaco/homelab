import polars as pl

import homelab.core.dataset.bronze.scryfall
import homelab.core.endpoint.scryfall
from homelab.extract.scryfall import ExtractScryfall


class ExtractScryfallCards(ExtractScryfall):
    def __init__(self) -> None:
        super().__init__(
            endpoint=homelab.core.endpoint.scryfall.cards,
            dataset=homelab.core.dataset.bronze.scryfall.cards,
        )

    def get_data(self) -> pl.DataFrame:
        data = self.api_client.get(
            endpoint=self.endpoint,
            params={"q": "legal:pioneer"},
        )

        return pl.DataFrame(
            data=data,
            infer_schema_length=len(data),
        )


if __name__ == "__main__":
    ExtractScryfallCards().run()
