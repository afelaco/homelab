import urllib.parse
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


def get_deck_color_identity(deck_full_df: pl.DataFrame) -> list[str]:
    """Extracts unique color symbols (W, U, B, R, G) present in the deck."""
    colors = set()
    for col_val in deck_full_df.select("color").drop_nulls().to_series().to_list():
        if col_val:
            for ch in str(col_val).strip():
                if ch.upper() in {"W", "U", "B", "R", "G"}:
                    colors.add(ch.upper())

    order = {"W": 0, "U": 1, "B": 2, "R": 3, "G": 4}
    return sorted(list(colors), key=lambda x: order.get(x, 99))


def render_mana_icons_html(colors: list[str]) -> str:
    """Generates inline HTML img tags for Scryfall SVGs for each color present."""
    if not colors:
        return '<img src="https://svgs.scryfall.io/card-symbols/C.svg" style="width: 28px; height: 28px; vertical-align: middle;">'

    html_snippets = []
    for c in colors:
        svg_url = f"https://svgs.scryfall.io/card-symbols/{c}.svg"
        html_snippets.append(
            f'<img src="{svg_url}" style="width: 28px; height: 28px; vertical-align: middle; margin-left: 6px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.6));">'
        )
    return "".join(html_snippets)


def get_copy_tier_info(quantity: int, cmc: float | int | None) -> tuple[str, str, str, str, int]:
    """
    Maps card copy quantity and CMC to rulebook tiers.
    Overrides low-count cards with CMC >= 5 to 'Finisher'.
    Returns: (tier_label, badge_color, bg_rgba, bar_gradient, fill_pct)
    """
    is_high_cmc = cmc is not None and cmc >= 5

    if quantity >= 4:
        return "Core Synergy", "#00c853", "rgba(0, 200, 83, 0.15)", "linear-gradient(90deg, #00c853, #69f0ae)", 100
    elif quantity == 3:
        return "Important", "#ffd600", "rgba(255, 214, 0, 0.15)", "linear-gradient(90deg, #ffd600, #ffff8d)", 75
    elif quantity == 2:
        if is_high_cmc:
            return "Finisher", "#e040fb", "rgba(224, 64, 251, 0.15)", "linear-gradient(90deg, #e040fb, #ea80fc)", 50
        return "Situational", "#ff9100", "rgba(255, 145, 0, 0.15)", "linear-gradient(90deg, #ff9100, #ffab40)", 50
    else:
        if is_high_cmc:
            return "Finisher", "#e040fb", "rgba(224, 64, 251, 0.15)", "linear-gradient(90deg, #e040fb, #ea80fc)", 25
        return "Silver Bullet", "#00b0ff", "rgba(0, 176, 255, 0.15)", "linear-gradient(90deg, #00b0ff, #80d8ff)", 25


def classify_card_type(type_str: str) -> str:
    """Normalizes card type string into clean high-level categories."""
    if not type_str or not isinstance(type_str, str):
        return "Other"
    t = type_str.lower()
    if "creature" in t:
        return "Creatures"
    elif "land" in t:
        return "Lands"
    elif "instant" in t:
        return "Instants"
    elif "sorcery" in t:
        return "Sorceries"
    elif "artifact" in t:
        return "Artifacts"
    elif "enchantment" in t:
        return "Enchantments"
    elif "planeswalker" in t:
        return "Planeswalkers"
    elif "battle" in t:
        return "Battles"
    return "Other"


def render_card_subgrid(cards_pd):
    """Renders a subset of cards in a responsive 4-column Streamlit grid."""
    if cards_pd.empty:
        st.info("No cards found in this group.")
        return

    cols = st.columns(4)
    for idx, row in cards_pd.reset_index(drop=True).iterrows():
        card_name = row["card_name"]
        quantity = int(row["quantity"])
        cmc_val = row.get("cmc")

        front_face_name = str(card_name).split("//")[0].strip()
        image_url = get_card_image_url(card_name, row.get("image_url"))

        scryfall_url = row.get("scryfall_url")
        if not (scryfall_url and isinstance(scryfall_url, str) and scryfall_url.strip()):
            encoded_link_name = urllib.parse.quote(front_face_name)
            scryfall_url = f"https://scryfall.com/search?q=%21%22{encoded_link_name}%22"

        raw_tags = row.get("tags")
        if isinstance(raw_tags, str):
            tags_list = [raw_tags]
        elif raw_tags is not None and hasattr(raw_tags, "__iter__"):
            tags_list = list(raw_tags)
        else:
            tags_list = []

        tags_html = "".join([
            f'<span style="background: rgba(255,75,75,0.15); color: #ff7b7b; padding: 2px 6px; border-radius: 4px; display: inline-block; margin: 2px;">{t}</span>'
            for t in tags_list
        ]) if tags_list else '<span style="color: #888;">No tags recorded</span>'

        tier_label, badge_color, bg_rgba, bar_gradient, fill_pct = get_copy_tier_info(quantity, cmc_val)

        with cols[idx % 4]:
            has_valid_link = bool(scryfall_url and isinstance(scryfall_url, str) and scryfall_url.strip())
            link_prefix = f'<a href="{scryfall_url}" target="_blank">' if has_valid_link else ''
            link_suffix = '</a>' if has_valid_link else ''

            st.markdown(
                f'''
                <div class="mtg-card-wrap">
                    <div class="mtg-tooltip">
                        <div style="font-weight: 700; margin-bottom: 4px; color: #a0a6b2; text-transform: uppercase; font-size: 0.7rem;">Card Tags</div>
                        <div>{tags_html}</div>
                    </div>
                    {link_prefix}
                        <img src="{image_url}" style="width: 100%; border-radius: 8px; margin-bottom: 6px; display: block;">
                    {link_suffix}
                </div>
                ''',
                unsafe_allow_html=True
            )

            # 4-3-2-1 Rulebook Tier Badge Frame
            st.markdown(
                f'''
                <div style="background-color: #1e222a; border: 1px solid #313640; border-radius: 6px; padding: 6px 10px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size: 0.8rem; font-weight: 700; color: #a0a6b2;">{quantity}x Copies</span>
                        <span style="font-size: 0.75rem; font-weight: 700; color: {badge_color}; background: {bg_rgba}; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">{tier_label}</span>
                    </div>
                    <div style="width: 100%; background-color: #2b303c; height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="width: {fill_pct}%; background: {bar_gradient}; height: 100%; border-radius: 3px;"></div>
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )


def render_summary_tab(deck_full_df: pl.DataFrame):
    colors = get_deck_color_identity(deck_full_df)
    mana_html = render_mana_icons_html(colors)

    # Clean Header Layout with Right-Aligned Color Identity Capsule Badge
    st.markdown(
        f'''
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid #313640;">
            <h3 style="margin: 0; font-family: 'Cinzel', serif; letter-spacing: 0.5px;">Automated Deck Audit & Rulebook Metrics</h3>
            <div style="display: flex; align-items: center; background-color: #1e222a; border: 1px solid #313640; padding: 6px 14px; border-radius: 20px;">
                <span style="font-size: 0.75rem; font-weight: 700; color: #a0a6b2; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Identity</span>
                <div style="display: flex; align-items: center;">{mana_html}</div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # 1. Core Rulebook Metrics Calculations
    total_cards = int(deck_full_df.select(pl.col("quantity").sum()).item())
    amv = calculate_amv(deck_full_df)
    actual_lands = calculate_actual_lands(deck_full_df)
    n_ramp_draw = detect_cheap_ramp_draw(deck_full_df)

    mdfc_cards_df = deck_full_df.filter(pl.col("card_name").str.contains(r"//"))
    n_untapped_mdfc = float(mdfc_cards_df.height)

    karsten_lands = calculate_karsten_lands(amv, n_ramp_draw, n_untapped_mdfc=n_untapped_mdfc)
    interaction_count, interaction_status = check_interaction_floor(deck_full_df)

    # 2. Metric Cards Display with Conditional Warning Borders
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f'''
            <div style="background-color: #16181d; border: 1px solid #313640; border-radius: 8px; padding: 16px; height: 100%;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #a0a6b2; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Total Cards</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff;">{total_cards}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f'''
            <div style="background-color: #16181d; border: 1px solid #313640; border-radius: 8px; padding: 16px; height: 100%;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #a0a6b2; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Non-Land AMV</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff;">{amv:.2f}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m3:
        land_border = "#ff9100" if abs(actual_lands - karsten_lands) > 2.0 else "#313640"
        st.markdown(
            f'''
            <div style="background-color: #16181d; border: 1px solid {land_border}; border-radius: 8px; padding: 16px; height: 100%;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #a0a6b2; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Karsten Land Target</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff;">{karsten_lands:.1f}</div>
                <div style="font-size: 0.8rem; color: #a0a6b2; margin-top: 4px;">{actual_lands - karsten_lands:+.1f} vs Actual ({actual_lands})</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m4:
        floor_border = "#ff4b4b" if interaction_count < 7 else "#313640"
        floor_color = "#ff4b4b" if interaction_count < 7 else "#00c853"
        st.markdown(
            f'''
            <div style="background-color: #16181d; border: 1px solid {floor_border}; border-radius: 8px; padding: 16px; height: 100%;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #a0a6b2; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Interaction Floor</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff;">{interaction_count} <span style="font-size: 1rem; font-weight: normal; color: #a0a6b2;">slots</span></div>
                <div style="font-size: 0.8rem; color: {floor_color}; margin-top: 4px;">{interaction_status}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown("---")
    deck_bar_color = get_deck_bar_color(deck_full_df)

    # 3. Side-by-Side Charts (Mana Curve & Top 10 Deck Tags with transparent background & fixed label limits)
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
                .configure(background="transparent", view=alt.ViewConfig(stroke=None))
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
                    y=alt.Y("tags:N", sort="-x", title="Tag Name", axis=alt.Axis(labelLimit=200)),
                    color=alt.value(deck_bar_color),
                    tooltip=["tags", "deck_count"]
                )
                .properties(height=320)
                .configure(background="transparent", view=alt.ViewConfig(stroke=None))
            )
            st.altair_chart(tag_chart, use_container_width=True)
        else:
            st.info("No card tags found for the cards in this decklist.")

    st.markdown("---")

    # 4. Section Header & Interactive Grouping Selectbox
    col_hdr, col_sel = st.columns([3, 2])
    with col_hdr:
        st.subheader("Parsed Decklist Card Grid")
    with col_sel:
        group_mode = st.selectbox(
            "Group view by",
            ["Flat Grid", "Card Type", "Mana Value (CMC)", "Card Tag"],
            label_visibility="collapsed",
            filter_mode=None
        )

    # 5. Injected CSS for Top-Anchored Hover Tooltips
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
            position: absolute;
            top: 8px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 999;
            width: 90%;
            background-color: rgba(22, 24, 29, 0.95);
            color: #ffffff;
            text-align: left;
            border-radius: 6px;
            padding: 8px 10px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.8);
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

    deck_pd = deck_full_df.to_pandas()

    # 6. Render Based on Selected Grouping Mode
    if group_mode == "Flat Grid":
        render_card_subgrid(deck_pd)

    elif group_mode == "Card Type":
        deck_pd["grouped_type"] = deck_pd["type"].apply(classify_card_type)
        type_order = ["Creatures", "Instants", "Sorceries", "Artifacts", "Enchantments", "Planeswalkers", "Lands",
                      "Battles", "Other"]

        for g_type in type_order:
            subset = deck_pd[deck_pd["grouped_type"] == g_type]
            if not subset.empty:
                st.markdown(f"#### 🏷️ {g_type} ({int(subset['quantity'].sum())} cards)")
                render_card_subgrid(subset)
                st.markdown("<br>", unsafe_allow_html=True)

    elif group_mode == "Mana Value (CMC)":
        deck_pd["grouped_cmc"] = deck_pd["cmc"].fillna(-1).astype(int)
        sorted_cmcs = sorted(deck_pd["grouped_cmc"].unique())

        for cmc_val in sorted_cmcs:
            subset = deck_pd[deck_pd["grouped_cmc"] == cmc_val]
            label = f"CMC {cmc_val}" if cmc_val >= 0 else "Lands / No CMC"
            if not subset.empty:
                st.markdown(f"#### ⚡ {label} ({int(subset['quantity'].sum())} cards)")
                render_card_subgrid(subset)
                st.markdown("<br>", unsafe_allow_html=True)

    elif group_mode == "Card Tag":
        exploded_df = deck_full_df.explode("tags")
        exploded_pd = exploded_df.to_pandas()
        exploded_pd["tags"] = exploded_pd["tags"].fillna("Untagged")
        unique_tags = sorted(exploded_pd["tags"].unique())

        for tag_val in unique_tags:
            subset = exploded_pd[exploded_pd["tags"] == tag_val]
            if not subset.empty:
                st.markdown(f"#### 🏷️ Tag: `{tag_val}` ({int(subset['quantity'].sum())} cards)")
                render_card_subgrid(subset)
                st.markdown("<br>", unsafe_allow_html=True)