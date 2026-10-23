from polars import String, Int64

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
