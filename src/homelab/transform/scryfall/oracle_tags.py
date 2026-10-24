import polars as pl

import homelab.core.dataset.bronze.scryfall
import homelab.core.dataset.silver.scryfall
from homelab.transform import Transform

# Tags to exclude from deck functional analysis
EXCLUDED_TAGS = {
    "alliteration",
    "art-matters",
    "artist-matters",
    "border-color-matters",
    "card-style-matters",
    "dnd-book",
    "dnd-character",
    "dnd-item",
    "dnd-monster",
    "dnd-spell",
    "doctor-who-episode-name",
    "doctor-who-episode-saga",
    "eponymous",
    "eponymous-planeswalker",
    "fallout-perk-name",
    "fallout-vault-saga",
    "flavor-matters",
    "flavor-text-matters",
    "game-name",
    "ip-matters",
    "magic-term-name",
    "marvel-storyline-name",
    "mathy-name",
    "meme",
    "mob-name",
    "name-matters",
    "named-choice",
    "named-token",
    "namesake-spell",
    "onomatopoeia",
    "punny-name",
    "quote-name",
    "real-life-animal-name",
    "rhyming-name",
    "school-name",
    "shares-name-with-a-format",
    "shares-name-with-a-mechanic",
    "shares-name-with-a-set",
    "single-english-word-name",
    "sports-name",
    "three-letter-name",
    "tongue-twister",
    "checklist-card",
    "collector-number-matters",
    "cover-card",
    "deck-requirement",
    "digital-only-mechanics",
    "digital-replacement",
    "digital-to-paper",
    "draft-matters",
    "extra-draft",
    "format-matters",
    "front-card",
    "paper-compatible",
    "reminder-card",
    "stronger-in-singleton-formats",
    "substitute-card",
    "unprinted-token",
    "useless-in-singleton-formats",
    "weaker-in-singleton-formats",
    "external-prop",
    "fun-ruling",
    "functional-art",
    "guest-designer",
    "great-designer-search-3",
    "invitational-card",
    "other-games-matter",
    "sleeves-matter",
    "speech-matters",
    "un-color",
    "un-forecast",
    "un-keyword",
    "un-psychographics",
    "un-set-mechanics",
    "un-type-line",
    "unstable-killbot",
    "unstable-secret-base",
    "vanity-card",
    "type-errata",
    "virtual-french-vanilla",
    "flavors-of-vanilla",
    "card-names",
    "virtual-legendary",
    "40k-model",
    "5c-set-mechanic-commander",
}


class TransformScryfallOracleTags(Transform):
    def __init__(self) -> None:
        super().__init__(
            bronze_dataset=homelab.core.dataset.bronze.scryfall.oracle_tags,
            silver_dataset=homelab.core.dataset.silver.scryfall.oracle_tags,
            mapping={
                "id": "tag_id",
                "slug": "tag",
            },
        )

    def get_data(self) -> pl.DataFrame:
        data = (
            self.bronze_dataset.read_parquet()
            .rename(self.mapping)
            .filter(
                ~pl.col("tag").str.starts_with("cycle"),
                ~pl.col("tag").is_in(EXCLUDED_TAGS),
            )
        )

        direct_tags = self.get_direct_tags(data=data)
        parent_tags = self.get_parent_tags(data=data)

        return pl.concat([direct_tags, parent_tags]).filter(pl.col("tag").is_not_null())

    def get_direct_tags(self, data: pl.DataFrame) -> pl.DataFrame:
        return data.explode("taggings").unnest("taggings").sort("oracle_id").select(self.silver_dataset.schema.keys())

    def get_parent_tags(self, data: pl.DataFrame) -> pl.DataFrame:
        return (
            (
                data.explode("parent_ids")
                .explode("taggings")
                .unnest("taggings")
                .select(
                    "oracle_id",
                    pl.col("parent_ids").alias("tag_id"),
                    pl.col("weight"),
                )
            )
            .join(
                other=data.select(
                    "tag_id",
                    "tag",
                    "description",
                ),
                on="tag_id",
                how="left",
            )
            .select(self.silver_dataset.schema.keys())
        )


if __name__ == "__main__":
    TransformScryfallOracleTags().run()
