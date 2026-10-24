import urllib.parse
import polars as pl
import streamlit as st
from core.scryfall import get_card_image_url


def get_available_types(df: pl.DataFrame) -> list[str]:
    """Extracts clean base card types (Creature, Artifact, Enchantment, etc.) from type lines."""
    base_types = {"Creature", "Artifact", "Enchantment", "Instant", "Sorcery", "Planeswalker", "Land", "Battle"}
    found_types = set()
    for t in df.select("type").drop_nulls().to_series().to_list():
        if t and isinstance(t, str):
            for bt in base_types:
                if bt.lower() in t.lower():
                    found_types.add(bt)
    return sorted(list(found_types))


def get_available_subtypes(df: pl.DataFrame) -> list[str]:
    """Extracts unique card subtypes from the type line."""
    subtypes = set()
    for t in df.select("type").drop_nulls().to_series().to_list():
        if t and isinstance(t, str) and "—" in t:
            parts = t.split("—")
            if len(parts) > 1:
                sub_part = parts[1].strip()
                for sub in sub_part.split():
                    clean_sub = sub.strip(" ,.")
                    if clean_sub:
                        subtypes.add(clean_sub)
    return sorted(list(subtypes))


def render_mana_icons_html(colors: set) -> str:
    """Generates inline HTML img tags for Scryfall SVGs for each color present."""
    if not colors:
        return '<img src="https://svgs.scryfall.io/card-symbols/C.svg" style="width: 28px; height: 28px; vertical-align: middle;">'

    order = {"W": 0, "U": 1, "B": 2, "R": 3, "G": 4}
    sorted_colors = sorted(list(colors), key=lambda x: order.get(x, 99))

    html_snippets = []
    for c in sorted_colors:
        svg_url = f"https://svgs.scryfall.io/card-symbols/{c}.svg"
        html_snippets.append(
            f'<img src="{svg_url}" style="width: 28px; height: 28px; vertical-align: middle; margin-left: 6px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.6));">'
        )
    return "".join(html_snippets)


def get_synergy_tier_info(score: float, max_score: float) -> tuple[str, str, str]:
    """
    Categorizes synergy scores into visual tiers based on max score percentage:
    - Max score: Purple (👑)
    - >= 90% of max: Green (🔥)
    - < 90% and >= 66% of max: Yellow (⚡)
    - < 66% of max: Red (💡)
    Returns: (icon, text_color, bar_gradient)
    """
    ratio = score / max_score if max_score > 0 else 0.0

    if score >= max_score - 1e-5 and max_score > 0:
        return "👑", "#e040fb", "linear-gradient(90deg, #e040fb, #ea80fc)"
    elif ratio >= 0.90:
        return "🔥", "#00c853", "linear-gradient(90deg, #00c853, #69f0ae)"
    elif ratio >= 0.66:
        return "⚡", "#ffd600", "linear-gradient(90deg, #ffd600, #ffff8d)"
    else:
        return "💡", "#ff4b4b", "linear-gradient(90deg, #ff4b4b, #ff8a80)"


def render_recommendations_tab(recommended_df: pl.DataFrame, deck_allowed_colors: set):
    """Renders the recommendation tab with color identity headers, robust sidebar filters, and dynamic score bars."""
    mana_html = render_mana_icons_html(deck_allowed_colors)

    # Clean Header Layout without Bottom Border
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
            <h3 style="margin: 0; font-family: 'Cinzel', serif; letter-spacing: 0.5px;">Synergy Recommendations</h3>
            <div style="display: flex; align-items: center; background-color: #1e222a; border: 1px solid #313640; padding: 6px 14px; border-radius: 20px;">
                <span style="font-size: 0.75rem; font-weight: 700; color: #a0a6b2; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Identity</span>
                <div style="display: flex; align-items: center;">{mana_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if recommended_df.is_empty():
        st.info("No recommendations found. Try adding more cards to your decklist!")
        return

    # --- SIDEBAR / TOP FILTERS ---
    st.sidebar.markdown("### 🎛️ Filter Recommendations")

    # 1. Card Type Filter
    available_types = get_available_types(recommended_df)
    selected_types = st.sidebar.multiselect("Card Type", options=available_types)

    # 2. Card Subtype Filter
    available_subtypes = get_available_subtypes(recommended_df)
    selected_subtypes = st.sidebar.multiselect("Card Subtype (e.g., Angel, Cleric, Aura)", options=available_subtypes)

    # 3. Synergy Tag Filter (matching_tags)
    all_matching_tags = sorted(
        recommended_df.select(pl.col("matching_tags").list.explode())
        .drop_nulls()
        .unique()
        .to_series()
        .to_list()
    )
    selected_tags = st.sidebar.multiselect("Synergy Tag (e.g., life-gain, ramp)", options=all_matching_tags)

    # 4. Dynamic CMC Range Slider (0 to max CMC in recommendations)
    max_cmc_val = int(recommended_df.select(pl.col("cmc").max()).item() or 10)
    min_cmc_val = int(recommended_df.select(pl.col("cmc").min()).item() or 0)

    cmc_range = st.sidebar.slider(
        "Mana Value (CMC)",
        min_value=min_cmc_val,
        max_value=max_cmc_val,
        value=(min_cmc_val, max_cmc_val),
    )

    # --- APPLY FILTERS ---
    filtered_df = recommended_df

    if selected_types:
        type_expr = pl.any_horizontal([pl.col("type").str.contains(t, literal=True) for t in selected_types])
        filtered_df = filtered_df.filter(type_expr)

    if selected_subtypes:
        subtype_expr = pl.any_horizontal([pl.col("type").str.contains(sub, literal=True) for sub in selected_subtypes])
        filtered_df = filtered_df.filter(subtype_expr)

    if selected_tags:
        filtered_df = filtered_df.filter(
            pl.col("matching_tags").list.eval(pl.element().is_in(selected_tags)).list.any()
        )

    # Apply CMC range filter
    filtered_df = filtered_df.filter((pl.col("cmc") >= cmc_range[0]) & (pl.col("cmc") <= cmc_range[1]))

    st.markdown(f"Showing **{filtered_df.height}** recommendations matching your filter criteria.")

    if filtered_df.is_empty():
        st.warning("No cards match the selected filter criteria.")
        return

    # Determine maximum score for relative progress bar scaling
    max_score = float(filtered_df.select(pl.col("synergy_score").max()).item() or 1.0)
    if max_score <= 0:
        max_score = 1.0

    # Injected CSS for Hover Tooltips
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
        unsafe_allow_html=True,
    )

    # --- RENDER RECOMMENDATIONS GRID ---
    recommendations_pd = filtered_df.to_pandas()
    cols = st.columns(4)

    for idx, row in recommendations_pd.reset_index(drop=True).iterrows():
        card_name = row["card_name"]
        score = float(row["synergy_score"])

        front_face_name = str(card_name).split("//")[0].strip()
        image_url = get_card_image_url(card_name, row.get("image_url"))

        scryfall_url = row.get("scryfall_url")
        if not (scryfall_url and isinstance(scryfall_url, str) and scryfall_url.strip()):
            encoded_link_name = urllib.parse.quote(front_face_name)
            scryfall_url = f"https://scryfall.com/search?q=%21%22{encoded_link_name}%22"

        raw_tags = row.get("matching_tags")
        if isinstance(raw_tags, str):
            tags_list = [raw_tags]
        elif raw_tags is not None and hasattr(raw_tags, "__iter__"):
            tags_list = list(raw_tags)
        else:
            tags_list = []

        tags_html = (
            "".join([
                f'<span style="background: rgba(0,200,83,0.15); color: #00c853; padding: 2px 6px; border-radius: 4px; display: inline-block; margin: 2px;">{t}</span>'
                for t in tags_list
            ])
            if tags_list
            else '<span style="color: #888;">No matching tags</span>'
        )

        icon, text_color, bar_gradient = get_synergy_tier_info(score, max_score)
        fill_pct = min(100.0, max(5.0, (score / max_score) * 100))

        with cols[idx % 4]:
            has_valid_link = bool(scryfall_url and isinstance(scryfall_url, str) and scryfall_url.strip())
            link_prefix = f'<a href="{scryfall_url}" target="_blank">' if has_valid_link else ""
            link_suffix = "</a>" if has_valid_link else ""

            st.markdown(
                f"""
                <div class="mtg-card-wrap">
                    <div class="mtg-tooltip">
                        <div style="font-weight: 700; margin-bottom: 4px; color: #a0a6b2; text-transform: uppercase; font-size: 0.7rem;">Matching Synergy Tags</div>
                        <div>{tags_html}</div>
                    </div>
                    {link_prefix}
                        <img src="{image_url}" style="width: 100%; border-radius: 8px; margin-bottom: 6px; display: block;">
                    {link_suffix}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Card Score Box with Integer Score & Tier Icon
            st.markdown(
                f"""
                <div style="background-color: #1e222a; border: 1px solid #313640; border-radius: 6px; padding: 6px 10px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size: 0.8rem; font-weight: 700; color: {text_color};">Score: {int(score)}</span>
                        <span style="font-size: 1rem;">{icon}</span>
                    </div>
                    <div style="width: 100%; background-color: #2b303c; height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="width: {fill_pct}%; background: {bar_gradient}; height: 100%; border-radius: 3px;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )