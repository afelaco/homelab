import streamlit as st
import polars as pl
from core.scryfall import get_card_image_url

def render_recommendations_tab(recommended_df: pl.DataFrame, deck_allowed_colors: set):
    color_identity_str = "".join(sorted(deck_allowed_colors)) if deck_allowed_colors else "Colorless"

    st.subheader("Synergy Card Recommendations")
    st.caption(f"🎨 Inferred Deck Color Identity (`{color_identity_str}`)")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Filter Recommendations")

    selected_types = st.sidebar.multiselect(
        "Card Type",
        options=["Creature", "Instant", "Sorcery", "Enchantment", "Artifact", "Planeswalker", "Land"]
    )

    unique_cmcs = sorted([int(x) for x in recommended_df.select("cmc").drop_nulls().unique().to_series().to_list()])
    selected_cmcs = st.sidebar.multiselect("Mana Value (CMC)", options=unique_cmcs)

    filtered_df = recommended_df

    if selected_types:
        type_conditions = [pl.col("type").str.contains(f"(?i){t}") for t in selected_types]
        type_filter = type_conditions[0]
        for cond in type_conditions[1:]:
            type_filter = type_filter | cond
        filtered_df = filtered_df.filter(type_filter)

    if selected_cmcs:
        filtered_df = filtered_df.filter(pl.col("cmc").is_in(selected_cmcs))

    if filtered_df.is_empty():
        st.info("No synergy recommendations found matching your current filter criteria.")
    else:
        recs_pd = filtered_df.to_pandas()
        cols = st.columns(4)
        for idx, row in recs_pd.iterrows():
            card_name = row["card_name"]
            score = row["synergy_score"]
            image_url = get_card_image_url(card_name, row.get("image_url"))
            scryfall_url = row.get("scryfall_url")

            with cols[idx % 4]:
                has_valid_link = scryfall_url and isinstance(scryfall_url, str) and scryfall_url.strip()

                if has_valid_link:
                    st.markdown(
                        f'<a href="{scryfall_url}" target="_blank">'
                        f'<img src="{image_url}" style="width: 100%; border-radius: 4px; margin-bottom: 8px;">'
                        f'</a>',
                        unsafe_allow_html=True
                    )
                else:
                    st.image(image_url, width="stretch")

                caption_text = f"**[{card_name}]({scryfall_url})**\nSynergy Score: `{score}`" if has_valid_link else f"**{card_name}**\nSynergy Score: `{score}`"
                st.caption(caption_text)