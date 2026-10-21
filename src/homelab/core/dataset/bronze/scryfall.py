from homelab.core.dataset import Dataset
from homelab.core.model.bronze.scryfall import CardsBronzeModel

cards = Dataset(
    layer="bronze",
    name="cards",
    model=CardsBronzeModel,
)
