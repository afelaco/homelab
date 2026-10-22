import polars as pl

import homelab.core.dataset.bronze.scryfall
import homelab.core.dataset.silver.scryfall
from homelab.transform import Transform

# Tags to exclude from deck functional analysis
EXCLUDED_TAGS = {
    # 1. Catch-all for print/set cycles
    # (You can also filter using string startswith: tag.startswith("cycle-"))
    # 2. Name, Flavor, Art & Aesthetics
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
    # 3. Draft, Format & Product Metadata
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
    # 4. Jokes, Un-sets & External References
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
}


class TransformScryfallOracleTags(Transform):
    def __init__(self) -> None:
        super().__init__(
            bronze_dataset=homelab.core.dataset.bronze.scryfall.oracle_tags,
            silver_dataset=homelab.core.dataset.silver.scryfall.oracle_tags,
            mapping={"id": "tag_id"},
        )

    def get_data(self) -> pl.DataFrame:
        data = (
            self.bronze_dataset.read_parquet()
            .rename(self.mapping)
            .filter(
                ~pl.col("slug").str.starts_with("cycle"),
                ~pl.col("slug").is_in(EXCLUDED_TAGS),
            )
            .explode("parent_ids", empty_as_null=True)
            .explode("taggings", empty_as_null=True)
            .unnest("taggings")
        )

        ## TODO: this doesn't work as parent tags still carry the metadata of children, need to join
        parent_data = data.drop("tag_id").rename({"parent_ids": "tag_id"})
        data = data.drop("parent_ids")

        return pl.concat([data, parent_data.select(data.columns)])


if __name__ == "__main__":
    TransformScryfallOracleTags().run()
