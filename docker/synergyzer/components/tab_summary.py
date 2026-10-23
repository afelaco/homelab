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


def get_deck_bar_color(deck_full_df: pl.DataFrame) -> str:
    """Detects the primary deck color from card color identities and maps to a theme hex code."""
    all_chars = set()
    for col_val in deck_full_df.select("color").drop_nulls().to_series().to_list():
        if col_val:
            for ch in str(col_val).strip():
                all_chars.add(ch.upper())

    if len(all_chars) == 1:
        c = list(all_chars)[0]
        return {
            "W": "#d1a33b",  # White / Gold
            "U": "#0e68ab",  # Blue
            "B": "#7c7774",  # Black
            "R": "#ff4b4b",  # Red
            "G": "#00c853"  # Green
        }.get(c, "#ff4b4b")
    elif "G" in all_chars:
        return "#00c853"
    elif "R" in all_chars:
        return "#ff4b4b"
    elif "U" in all_chars:
        return "#0e68ab"
    elif "W" in all_chars:
        return "#d1a33b"
    elif "B" in all_chars:
        return "#7c7774"
    return "#ff4b4b"  # Default fallback


def render_summary_tab(deck_full_df: pl.DataFrame):
    st.subheader("Automated Deck Audit & Rulebook Metrics")

    # 1. Core Rulebook Metrics Calculations
    total_cards = int(deck_full_df.select(pl.col("quantity").sum()).item())
    amv = calculate_amv(deck_full_df)
    actual_lands = calculate_actual_lands(deck_full_df)
    n_ramp_draw = detect_cheap_ramp_draw(deck_full_df)

    mdfc_cards_df = deck_full_df.filter(pl.col("card_name").str.contains(r"//"))
    n_untapped_mdfc = float(mdfc_cards_df.height)

    karsten_lands = calculate_karsten_lands(amv, n_ramp_draw, n_untapped_mdfc=n_untapped_mdfc)
    interaction_count, interaction_status = check_interaction_floor(deck_full_df)

    # 2. Metric Cards Display
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Cards", total_cards)
    m2.metric("Non-Land AMV", f"{amv:.2f}")
    m3.metric(
        "Karsten Land Target",
        f"{karsten_lands:.1f}",
        delta=f"{actual_lands - karsten_lands:+.1f} vs Actual ({actual_lands})"
    )
    m4.metric(
        label="Interaction Floor",
        value=f"{interaction_count} slots",
        delta=interaction_status,
        delta_color="normal"
    )

    st.markdown("---")

    # Determine dynamic bar color based on deck colors
    deck_bar_color = get_deck_bar_color(deck_full_df)

    # 3. Side-by-Side Charts (Mana Curve & Top 10 Deck Tags)
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### Non-Land Mana Curve")
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
            curve_chart = (
                alt.Chart(curve_df)
                .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                .encode(
                    x=alt.X("cmc:N", title="Mana Value (CMC)", sort=None),
                    y=alt.Y("quantity:Q", title="Card Count"),
                    color=alt.value(deck_bar_color),
                    tooltip=["cmc", "quantity"]
                )
                .properties(height=320)
            )
            st.altair_chart(curve_chart, use_container_width=True)
        else:
            st.info("No non-land CMC data available for curve.")

    with col_right:
        st.markdown("#### Top 10 Deck Tags")
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
                .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
                .encode(
                    x=alt.X("deck_count:Q", title="Occurrence Count"),
                    y=alt.Y("tags:N", sort="-x", title="Tag Name"),
                    color=alt.value(deck_bar_color),
                    tooltip=["tags", "deck_count"]
                )
                .properties(height=320)
            )
            st.altair_chart(tag_chart, use_container_width=True)
        else:
            st.info("No card tags found for the cards in this decklist.")

    st.markdown("---")
    st.subheader("Parsed Decklist Card Grid")

    # 4. Injected CSS for Cursor-Following Hover Tooltips
    st.markdown(
        """
        <style>
        .mtg-card-wrap {
            position: relative;
            display: inline-block;
            width: 100%;
        }
        .mtg-tooltip {
            display: none;
            position: fixed;
            z-index: 9999;
            background-color: rgba(22, 24, 29, 0.95);
            color: #ffffff;
            text-align: left;
            border-radius: 6px;
            padding: 8px 12px;
            max-width: 260px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.7);
            border: 1px solid #313640;
            font-size: 0.75rem;
            pointer-events: none;
        }
        .mtg-card-wrap:hover .mtg-tooltip {
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 5. Render Card Grid
    deck_pd = deck_full_df.to_pandas()
    deck_cols = st.columns(4)
    for idx, row in deck_pd.iterrows():
        card_name = row["card_name"]
        quantity = row["quantity"]
        image_url = get_card_image_url(card_name, row.get("image_url"))
        scryfall_url = row.get("scryfall_url")

        raw_tags = row.get("tags")
        tags_list = list(raw_tags) if raw_tags is not None and hasattr(raw_tags, "__iter__") else []
        tags_html = "".join([
            f'<span style="background: rgba(255,75,75,0.15); color: #ff7b7b; padding: 2px 6px; border-radius: 4px; display: inline-block; margin: 2px;">{t}</span>'
            for t in tags_list
        ]) if tags_list else '<span style="color: #888;">No tags recorded</span>'

        with deck_cols[idx % 4]:
            has_valid_link = scryfall_url and isinstance(scryfall_url, str) and scryfall_url.strip()
            link_prefix = f'<a href="{scryfall_url}" target="_blank">' if has_valid_link else ''
            link_suffix = '</a>' if has_valid_link else ''

            card_id = f"summary-card-{idx}"

            st.markdown(
                f'''
                <div class="mtg-card-wrap" id="{card_id}" onmousemove="
                    let tip = this.querySelector('.mtg-tooltip');
                    if (tip) {{
                        tip.style.left = (event.clientX + 12) + 'px';
                        tip.style.top = (event.clientY + 12) + 'px';
                    }}
                ">
                    <div class="mtg-tooltip">
                        <div style="font-weight: 700; margin-bottom: 4px; color: #a0a6b2; text-transform: uppercase; font-size: 0.7rem;">Card Tags</div>
                        <div>{tags_html}</div>
                    </div>
                    {link_prefix}
                        <img src="{image_url}" style="width: 100%; border-radius: 8px; margin-bottom: 4px;">
                    {link_suffix}
                </div>
                ''',
                unsafe_allow_html=True
            )

            caption_text = f"**{quantity}x** [{card_name}]({scryfall_url})" if has_valid_link else f"**{quantity}x** {card_name}"
            st.caption(caption_text)