import os
import json
import pathlib
import re
import streamlit as st
import polars as pl
from sqlalchemy import create_engine, text

st.set_page_config(
    page_title="Magic: The Gathering - Synergyzer",
    page_icon="🔮",
    layout="wide"
)

# ---------------------------------------------------------------------------
# Database Configuration & Connection
# ---------------------------------------------------------------------------
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")

POSTGRES_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@host.docker.internal:5432/postgres"

@st.cache_resource
def get_engine():
    return create_engine(POSTGRES_URL)

engine = get_engine()

# ---------------------------------------------------------------------------
# UI Layout & Sidebar Input
# ---------------------------------------------------------------------------
st.title("🔮 Magic: The Gathering - Synergyzer")

deck_text = st.sidebar.text_area(
    "ManaBox Decklist",
    value="[CREATURES]\n4 Speaker of the Heavens\n4 Bishop of Wings\n4 Giada, Font of Hope",
    height=300
)

def parse_manabox_text(text: str) -> pl.DataFrame:
    """Parses raw text box input using a strict regex pattern and skips category headers."""
    pattern = re.compile(r"^(\d+)\s+(.+)$")
    records = []

    for line in text.strip().splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("["):
            continue

        match = pattern.match(line_str)
        if match:
            copies = int(match.group(1))
            card_name = match.group(2).strip()
            records.append({"quantity": copies, "card_name": card_name})

    if not records:
        return pl.DataFrame(schema={"quantity": pl.Int64, "card_name": pl.Utf8})
    return pl.DataFrame(records)

def get_tag_synergy() -> pl.DataFrame:
    """Loads synergy mapping rules from the baked-in synergies.json file."""
    json_path = pathlib.Path("synergies.json")
    if json_path.exists():
        with open(json_path, "r") as f:
            raw_data = json.load(f)
        return pl.DataFrame(raw_data)
    else:
        st.error("synergies.json not found in container image.")
        return pl.DataFrame(schema={"tag_a": pl.Utf8, "tag_b": pl.Utf8})

# ---------------------------------------------------------------------------
# Recommendation Engine Pipeline
# ---------------------------------------------------------------------------
if st.sidebar.button("Analyze & Recommend", type="primary"):
    if not deck_text.strip():
        st.warning("Please provide a valid decklist.")
    else:
        deck_df = parse_manabox_text(deck_text)

        if deck_df.is_empty():
            st.warning("No valid cards found. Check your decklist formatting.")
        else:
            card_names = deck_df["card_name"].to_list()

            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("Parsed Decklist")
                st.dataframe(deck_df, use_container_width=True)

            try:
                with engine.connect() as conn:
                    # 1. Fetch database tags for the cards currently in the input decklist using exact schema keys
                    deck_tags_query = text("""
                        SELECT c.card AS card_name, t.tag AS tag
                        FROM dim_cards c
                        JOIN fact_cards_tags f ON c.oracle_id = f.oracle_id
                        JOIN dim_tags t ON f.tag_id = t.tag_id
                        WHERE c.card = ANY(:card_names);
                    """)
                    result = conn.execute(deck_tags_query, {"card_names": card_names})
                    deck_tags_df = pl.DataFrame(result.fetchall(), schema=list(result.keys()))

                    # 2. Fetch all cards and tags from the database to evaluate against synergy rules
                    all_cards_tags_query = text("""
                        SELECT c.card AS card_name, t.tag AS tag
                        FROM dim_cards c
                        JOIN fact_cards_tags f ON c.oracle_id = f.oracle_id
                        JOIN dim_tags t ON f.tag_id = t.tag_id;
                    """)
                    result_all = conn.execute(all_cards_tags_query)
                    all_cards_tags_df = pl.DataFrame(result_all.fetchall(), schema=list(result_all.keys()))

                with col2:
                    st.subheader("Synergy Card Recommendations")
                    if deck_tags_df.is_empty():
                        st.info("No matching database tags found for cards in this decklist.")
                    else:
                        # 3. Execute the Polars synergy join and aggregation pipeline
                        tags_synergies = get_tag_synergy()

                        recommended = (
                            deck_tags_df.select("tag")
                            .unique()
                            .join(other=tags_synergies, left_on="tag", right_on="tag_a", how="inner")
                            .join(other=all_cards_tags_df, left_on="tag_b", right_on="tag", how="inner")
                            .filter(~pl.col("card_name").is_in(card_names))  # Exclude cards already present in the deck
                            .group_by("card_name")
                            .agg(pl.count("tag_b").alias("synergy_score"))
                            .sort("synergy_score", descending=True)
                        )

                        if recommended.is_empty():
                            st.info("No synergy recommendations found for current deck tags.")
                        else:
                            st.dataframe(recommended.to_pandas(), use_container_width=True)

            except Exception as e:
                st.error(f"Database query or recommendation pipeline failed: {e}")