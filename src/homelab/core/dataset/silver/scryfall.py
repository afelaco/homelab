from homelab.core.dataset import Dataset
from homelab.core.model.silver.scryfall import CardsSilverModel

cards = Dataset(
    layer="silver",
    name="cards",
    model=CardsSilverModel,
)

