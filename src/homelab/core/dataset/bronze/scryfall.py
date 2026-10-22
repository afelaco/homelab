from homelab.core.dataset import Dataset
from homelab.core.model.bronze.scryfall import CardsBronzeModel, OracleTagsBronzeModel

cards = Dataset(
    layer="bronze",
    name="cards",
    model=CardsBronzeModel,
)
oracle_tags = Dataset(
    layer="bronze",
    name="oracle_tags",
    model=OracleTagsBronzeModel,
)
