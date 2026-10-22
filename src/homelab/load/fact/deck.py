import polars as pl

import homelab.core.dataset.silver.scryfall

cards = homelab.core.dataset.silver.scryfall.cards.read_parquet()
tags = homelab.core.dataset.silver.scryfall.oracle_tags.read_parquet()

deck = pl.DataFrame(
    [
        {"name": "Bishop of Wings", "copies": 4},
        {"name": "Cavern of Souls", "copies": 3},
        {"name": "Eiganjo, Seat of the Empire", "copies": 1},
        {"name": "Emeria's Call", "copies": 3},
        {"name": "Exemplar of Light", "copies": 4},
        {"name": "Giada, Font of Hope", "copies": 4},
        {"name": "Lyra Dawnbringer", "copies": 2},
        {"name": "Mutavault", "copies": 1},
        {"name": "Plains", "copies": 16},
        {"name": "Resplendent Angel", "copies": 4},
        {"name": "Restoration Magic", "copies": 4},
        {"name": "Righteous Valkyrie", "copies": 4},
        {"name": "Sejiri Shelter", "copies": 4},
        {"name": "Speaker of the Heavens", "copies": 4},
        {"name": "The Book of Exalted Deeds", "copies": 2},
    ]
)

ans = (
    deck.join(other=cards, on="name", how="left")
    .join(other=tags, on="oracle_id", how="left")
    .group_by("slug")
    .agg(pl.col("copies").sum())
    .sort("copies", descending=True)
    .to_pandas()
)
