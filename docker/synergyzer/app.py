import streamlit as st
from config import get_engine
from core.parser import parse_manabox_text
from engine.recommender import run_recommendation_pipeline
from components.tab_summary import render_summary_tab
from components.tab_recommendations import render_recommendations_tab

st.set_page_config(
    page_title="Magic: The Gathering - Synergyzer",
    layout="wide"
)

st.title("💎 Magic: The Gathering - Synergyzer")

engine = get_engine()

deck_text = st.sidebar.text_area(
    "ManaBox Decklist",
    value="[CREATURES]\n4 Speaker of the Heavens\n4 Bishop of Wings\n4 Giada, Font of Hope",
    height=300
)

if st.sidebar.button("Analyze & Recommend", type="primary"):
    if not deck_text.strip():
        st.warning("Please provide a valid decklist.")
    else:
        deck_df = parse_manabox_text(deck_text)

        if deck_df.is_empty():
            st.warning("No valid cards found. Check your decklist formatting.")
        else:
            try:
                deck_full_df, recommended_df, deck_allowed_colors = run_recommendation_pipeline(deck_df, engine)

                # Persist state
                st.session_state["deck_full_df"] = deck_full_df
                st.session_state["recommended_df"] = recommended_df
                st.session_state["deck_allowed_colors"] = deck_allowed_colors
            except Exception as e:
                st.error(f"Database query or recommendation pipeline failed: {e}")

# Render UI from Session State
if "recommended_df" in st.session_state:
    tab_summary, tab_recs = st.tabs(["📊 Deck Summary", "🔮 Synergy Recommendations"])

    with tab_summary:
        render_summary_tab(st.session_state["deck_full_df"])

    with tab_recs:
        render_recommendations_tab(st.session_state["recommended_df"], st.session_state["deck_allowed_colors"])