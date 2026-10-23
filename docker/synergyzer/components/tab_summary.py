import altair as alt
import streamlit as st
import polars as pl
from core.scryfall import get_card_image_url
from engine.metrics import (
    calculate_amv,
    calculate_actual_lands,
    detect_cheap_ramp_draw,
    calculate_karsten_lands,
    check_interaction_floor,
)

def render_summary_tab(deck_full_df: pl.DataFrame):
    st.subheader("Automated Deck Audit & Rulebook Metrics")

    total_cards = int(deck_full_df.select(pl.col("quantity").sum()).item())
    amv = calculate_amv(deck_full_df)
    actual_lands = calculate_actual_lands(deck_full_df)
    n_ramp_draw = detect_cheap_ramp_draw(deck_full_df)

    # Detect MDFC cards
    mdfc_cards_df = deck_full_df.filter(pl.col("card_name").str.contains(r"//"))
    n_untapped_mdfc = float(mdfc_cards_df.height)

    karsten_lands = calculate_karsten_lands(amv, n_ramp_draw, n_untapped_mdfc=n_untapped_mdfc)
    interaction_count, interaction_status = check_interaction_floor(deck_full_df)

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Cards", total_cards)
    m2.metric("Non-Land AMV", f"{amv:.2f}")
    m3.metric("Karsten Land Target", f"{karsten_lands:.1f}", delta=f"{actual_lands - karsten_lands:+.1f} vs Actual ({actual_lands})")
    m4.metric("Interaction Floor", f"{interaction_count} slots", delta=interaction_status)

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### Non-Land Mana Curve (CMC Distribution)")
        curve_df = (
            deck_full_df
            .filter((pl.col("cmc").is_not_null()) & (~pl.col("type").str.contains("(?i)land")))
            .group_by("cmc")
            .agg(pl.col("quantity").sum())
            .sort("cmc")
            .to_pandas()
        )
        if not curve_df.empty:
            curve_df["cmc"] = curve_df["cmc"].astype(int).astype(str)
            st.bar_chart(curve_df.set_index("cmc")["quantity"])
        else:
            st.info("No non-land CMC data available for curve.")

    with col_right:
        st.markdown("#### Copy Count Hierarchy (4-3-2-1 Breakdown)")
        copy_counts = (
            deck_full_df
            .group_by("quantity")
            .agg(pl.col("card_name").count().alias("unique_cards"))
            .sort("quantity", descending=True)
            .to_pandas()
        )
        if not copy_counts.empty:
            copy_counts["Tier"] = copy_counts["quantity"].map({
                4: "4x (Core Synergy)",
                3: "3x (Important)",
                2: "2x (Situational)",
                1: "1x (Silver Bullet)"
            }).fillna("Other Count")
            st.dataframe(copy_counts[["quantity", "unique_cards", "Tier"]], use_container_width=True)
        else:
            st.info("No copy count data available.")

    st.markdown("---")
    st.markdown("#### Top 10 Deck Tags (Ranked by Occurrence)")

    deck_tags_count_df = (
        deck_full_df
        .explode("tags")
        .filter(pl.col("tags").is_not_null())
        .group_by("tags")
        .agg(pl.col("quantity").sum().alias("deck_count"))
        .sort("deck_count", descending=True)
        .head(10)
        .to_pandas()
    )

    if not deck_tags_count_df.empty:
        tag_chart = (
            alt.Chart(deck_tags_count_df)
            .mark_bar()
            .encode(
                x=alt.X("deck_count:Q", title="Occurrence Count"),
                y=alt.Y("tags:N", sort="-x", title="Tag Name"),
                color=alt.value("#ff4b4b"),
                tooltip=["tags", "deck_count"]
            )
            .properties(height=350)
        )
        st.altair_chart(tag_chart, use_container_width=True)
    else:
        st.info("No card tags found for the cards in this decklist.")

    st.markdown("---")
    st.subheader("Parsed Decklist Card Grid")

    deck_pd = deck_full_df.to_pandas()
    deck_cols = st.columns(4)
    for idx, row in deck_pd.iterrows():
        card_name = row["card_name"]
        quantity = row["quantity"]
        image_url = get_card_image_url(card_name, row.get("image_url"))
        scryfall_url = row.get("scryfall_url")

        with deck_cols[idx % 4]:
            has_valid_link = scryfall_url and isinstance(scryfall_url, str) and scryfall_url.strip()

            if has_valid_link:
                st.markdown(
                    f'<a href="{scryfall_url}" target="_blank">'
                    f'<img src="{image_url}" style="width: 100%; border-radius: 4px; margin-bottom: 4px;">'
                    f'</a>',
                    unsafe_allow_html=True
                )
            else:
                st.image(image_url, width="stretch")

            caption_text = f"**{quantity}x** [{card_name}]({scryfall_url})" if has_valid_link else f"**{quantity}x** {card_name}"
            st.caption(caption_text)