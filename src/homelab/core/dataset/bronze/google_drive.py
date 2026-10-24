from polars import Int64, String

from homelab.core.dataset import Dataset

decks = Dataset(
    layer="bronze",
    name="decks",
    schema={
        "deck": String,
        "card": String,
        "copies": Int64,
    },
)
