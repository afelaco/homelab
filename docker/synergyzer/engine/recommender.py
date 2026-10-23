import json
import pathlib
import polars as pl
from sqlalchemy import text, Engine

def get_tag_synergy() -> pl.DataFrame:
    """Loads synergy mapping rules from synergies.json."""
    json_path = pathlib.Path("synergies.json")
    if json_path.exists():
        with open(json_path, "r") as f:
            raw_data = json.load(f)
        return pl.DataFrame(raw_data)
    return pl.DataFrame(schema={"tag_a": pl.Utf8, "tag_b": pl.Utf8})

def run_recommendation_pipeline(deck_df: pl.DataFrame, engine: Engine):
    """Fetches card attributes, infers color identity, and runs synergy joins."""
    card_names = deck_df["card_name"].to_list()

    with engine.connect() as conn:
        # 1. Fetch card attributes and tags
        deck_cards_query = text("""
            SELECT DISTINCT c.card AS card_name, c.image_url, c.scryfall_url, c.color, c.type, c.cmc, t.tag
            FROM dim_cards c
            LEFT JOIN fact_cards_tags f ON c.oracle_id = f.oracle_id
            LEFT JOIN dim_tags t ON f.tag_id = t.tag_id
            WHERE c.card = ANY(:card_names);
        """)
        result_deck = conn.execute(deck_cards_query, {"card_names": card_names})
        raw_deck_data = pl.DataFrame(result_deck.fetchall(), schema=list(result_deck.keys()))

        deck_info_df = (
            raw_deck_data
            .group_by(["card_name", "image_url", "scryfall_url", "color", "type", "cmc"])
            .agg(pl.col("tag").drop_nulls().alias("tags"))
        )
        deck_full_df = deck_df.join(deck_info_df, on="card_name", how="left")

        # 2. Fetch tags for color identity
        deck_tags_query = text("""
            SELECT c.card AS card_name, c.color, t.tag AS tag
            FROM dim_cards c
            JOIN fact_cards_tags f ON c.oracle_id = f.oracle_id
            JOIN dim_tags t ON f.tag_id = t.tag_id
            WHERE c.card = ANY(:card_names);
        """)
        result = conn.execute(deck_tags_query, {"card_names": card_names})
        deck_tags_df = pl.DataFrame(result.fetchall(), schema=list(result.keys()))

        # 3. Fetch candidate cards
        all_cards_tags_query = text("""
            SELECT c.card AS card_name, c.type, c.cmc, c.image_url, c.scryfall_url, c.color, t.tag AS tag
            FROM dim_cards c
            JOIN fact_cards_tags f ON c.oracle_id = f.oracle_id
            JOIN dim_tags t ON f.tag_id = t.tag_id;
        """)
        result_all = conn.execute(all_cards_tags_query)
        all_cards_tags_df = pl.DataFrame(result_all.fetchall(), schema=list(result_all.keys()))

    if deck_tags_df.is_empty():
        return deck_full_df, pl.DataFrame(), set()

    # Inferred deck color identity {C}
    deck_colors_list = deck_tags_df.select("color").unique().to_series().to_list()
    deck_allowed_colors = set()
    for col_val in deck_colors_list:
        if col_val:
            for char in str(col_val).strip():
                deck_allowed_colors.add(char)

    def is_color_allowed(val):
        if val is None or not str(val).strip():
            return True
        return all(ch in deck_allowed_colors for ch in str(val).strip())

    candidate_cards_df = (
        all_cards_tags_df
        .filter(~pl.col("card_name").is_in(card_names))
        .filter(pl.col("color").map_elements(is_color_allowed, return_dtype=pl.Boolean))
    )

    tags_synergies = get_tag_synergy()

    recommended = (
        deck_tags_df.select("tag")
        .join(other=tags_synergies, left_on="tag", right_on="tag_a", how="inner")
        .join(other=candidate_cards_df, left_on="tag_b", right_on="tag", how="inner")
        .group_by("card_name")
        .agg([
            pl.len().alias("synergy_score"),
            pl.first("type").alias("type"),
            pl.first("cmc").alias("cmc"),
            pl.first("image_url").alias("image_url"),
            pl.first("scryfall_url").alias("scryfall_url")
        ])
        .sort("synergy_score", descending=True)
    )

    return deck_full_df, recommended, deck_allowed_colors