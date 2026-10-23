import re
import streamlit as st
import polars as pl
from core.scryfall import get_card_image_url


def extract_subtypes(type_series: pl.Series) -> list[str]:
    """Extracts unique sorted subtypes from card type-lines."""
    subtypes = set()
    for raw_type in type_series.drop_nulls().to_list():
        if not isinstance(raw_type, str):
            continue
        parts = re.split(r"—|-", raw_type)
        if len(parts) > 1:
            for st_token in parts[1].strip().split():
                cleaned = st_token.strip()
                if cleaned:
                    subtypes.add(cleaned)
    return sorted(list(subtypes))


def extract_available_tags(recommended_df: pl.DataFrame) -> list[str]:
    """Extracts unique sorted synergy tags from recommended cards."""
    if "matching_tags" not in recommended_df.columns:
        return []
    all_tags = set()
    for tags_list in recommended_df.select("matching_tags").to_series().to_list():
        if tags_list:
            for t in tags_list:
                if t:
                    all_tags.add(str(t))
    return sorted(list(all_tags))


def render_recommendations_tab(recommended_df: pl.DataFrame, deck_allowed_colors: set):
    color_identity_str = "".join(sorted(deck_allowed_colors)) if deck_allowed_colors else "Colorless"

    st.subheader("Synergy Card Recommendations")
    st.caption(f"🎨 Inferred Deck Color Identity (`{color_identity_str}`)")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Filter Recommendations")

    # 1. Card Type Filter
    selected_types = st.sidebar.multiselect(
        "Card Type",
        options=["Creature", "Instant", "Sorcery", "Enchantment", "Artifact", "Planeswalker", "Land"]
    )

    # 2. Card Subtype Filter
    available_subtypes = extract_subtypes(recommended_df.select("type").to_series())
    selected_subtypes = st.sidebar.multiselect(
        "Card Subtype (e.g., Angel, Cleric, Aura)",
        options=available_subtypes
    )

    # 3. Synergy Tag Filter
    available_tags = extract_available_tags(recommended_df)
    selected_tags = st.sidebar.multiselect(
        "Synergy Tag (e.g., life-gain, ramp)",
        options=available_tags
    )

    # 4. Mana Value (CMC) Filter
    unique_cmcs = sorted([int(x) for x in recommended_df.select("cmc").drop_nulls().unique().to_series().to_list()])
    selected_cmcs = st.sidebar.multiselect("Mana Value (CMC)", options=unique_cmcs)

    # Apply Filters
    filtered_df = recommended_df

    if selected_types:
        type_conditions = [pl.col("type").str.contains(f"(?i){t}") for t in selected_types]
        type_filter = type_conditions[0]
        for cond in type_conditions[1:]:
            type_filter = type_filter | cond
        filtered_df = filtered_df.filter(type_filter)

    if selected_subtypes:
        subtype_conditions = [pl.col("type").str.contains(f"(?i){st_val}") for st_val in selected_subtypes]
        subtype_filter = subtype_conditions[0]
        for cond in subtype_conditions[1:]:
            subtype_filter = subtype_filter | cond
        filtered_df = filtered_df.filter(subtype_filter)

    if selected_tags:
        # Filters recommendations that contain any of the selected synergy tags
        tag_filter = pl.col("matching_tags").list.eval(pl.element().is_in(selected_tags)).list.any()
        filtered_df = filtered_df.filter(tag_filter)

    if selected_cmcs:
        filtered_df = filtered_df.filter(pl.col("cmc").is_in(selected_cmcs))

    if filtered_df.is_empty():
        st.info("No synergy recommendations found matching your current filter criteria.")
    else:
        recs_pd = filtered_df.to_pandas()
        max_score = max(recs_pd["synergy_score"].max(), 1)

        cols = st.columns(4)
        for idx, row in recs_pd.iterrows():
            card_name = row["card_name"]
            score = int(row["synergy_score"])
            image_url = get_card_image_url(card_name, row.get("image_url"))
            scryfall_url = row.get("scryfall_url")

            matching_tags = row.get("matching_tags")
            tags_list = list(matching_tags) if matching_tags is not None and hasattr(matching_tags, "__iter__") else []
            tags_html = "".join([
                                    f'<span style="background: rgba(0,200,83,0.15); color: #69f0ae; padding: 2px 6px; border-radius: 4px; display: inline-block; margin: 2px;">{t}</span>'
                                    for t in
                                    tags_list]) if tags_list else '<span style="color: #888;">No matching tags</span>'

            pct = min(100, int((score / max_score) * 100))

            if pct >= 75:
                badge_icon = "🔥"
                badge_color = "#00c853"
                bg_rgba = "rgba(0, 200, 83, 0.15)"
                bar_gradient = "linear-gradient(90deg, #00c853, #69f0ae)"
            elif pct >= 40:
                badge_icon = "⚡"
                badge_color = "#ffd600"
                bg_rgba = "rgba(255, 214, 0, 0.15)"
                bar_gradient = "linear-gradient(90deg, #ffd600, #ffff8d)"
            else:
                badge_icon = "✨"
                badge_color = "#ff4b4b"
                bg_rgba = "rgba(255, 75, 75, 0.15)"
                bar_gradient = "linear-gradient(90deg, #ff4b4b, #ff7b7b)"

            with cols[idx % 4]:
                has_valid_link = scryfall_url and isinstance(scryfall_url, str) and scryfall_url.strip()
                link_prefix = f'<a href="{scryfall_url}" target="_blank">' if has_valid_link else ''
                link_suffix = '</a>' if has_valid_link else ''

                st.markdown(
                    f'''
                    <div class="mtg-card-wrap">
                        <div class="mtg-tooltip">
                            <div style="font-weight: 700; margin-bottom: 4px; color: #a0a6b2; text-transform: uppercase; font-size: 0.7rem;">Matching Synergy Tags</div>
                            <div>{tags_html}</div>
                        </div>
                        {link_prefix}
                            <img src="{image_url}" style="width: 100%; border-radius: 8px; margin-bottom: 6px;">
                        {link_suffix}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'''
                    <div style="background-color: #1e222a; border: 1px solid #313640; border-radius: 6px; padding: 6px 10px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <span style="font-size: 0.8rem; font-weight: 600; color: #a0a6b2; text-transform: uppercase; letter-spacing: 0.5px;">Synergy</span>
                            <span style="font-size: 0.85rem; font-weight: 700; color: {badge_color}; background: {bg_rgba}; padding: 2px 8px; border-radius: 4px;">{badge_icon} {score}</span>
                        </div>
                        <div style="width: 100%; background-color: #2b303c; height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="width: {pct}%; background: {bar_gradient}; height: 100%; border-radius: 3px;"></div>
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )