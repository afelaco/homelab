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

# Global SaaS-grade Styling & App-mode Framing
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Custom container styling for metrics */
    div[data-testid="stMetric"] {
        background-color: #1e222a;
        border: 1px solid #313640;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] label {
        color: #a0a6b2 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Card hover zoom and shadow */
    .mtg-card-wrap img {
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    .mtg-card-wrap:hover img {
        transform: scale(1.03);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
        border-color: #4a5260;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💎 Magic: The Gathering - Synergyzer")

engine = get_engine()

deck_text = st.sidebar.text_area(
    "ManaBox Decklist",
    value="[CREATURES]\n4 Speaker of the Heavens\n4 Bishop of Wings\n4 Giada, Font of Hope",
    height=300
)

# 1. Initialize session state deck if it doesn't exist yet
if "deck_df" not in st.session_state:
    st.session_state.deck_df = parse_manabox_text(deck_text)

# 2. Handle sidebar analysis button click
if st.sidebar.button("Analyze & Recommend", type="primary"):
    if not deck_text.strip():
        st.warning("Please provide a valid decklist.")
    else:
        parsed_df = parse_manabox_text(deck_text)
        if parsed_df.is_empty():
            st.warning("No valid cards found. Check your decklist formatting.")
        else:
            st.session_state.deck_df = parsed_df
            st.rerun()

# 3. Automatically run pipeline and render tabs whenever deck_df is present in session state
if "deck_df" in st.session_state and not st.session_state.deck_df.is_empty():
    try:
        deck_full_df, recommended_df, deck_allowed_colors = run_recommendation_pipeline(
            st.session_state.deck_df, engine
        )

        tab_summary, tab_recs = st.tabs(["📊 Deck Summary", "🔮 Synergy Recommendations"])

        with tab_summary:
            render_summary_tab(deck_full_df)

        with tab_recs:
            render_recommendations_tab(recommended_df, deck_allowed_colors)

    except Exception as e:
        st.error(f"Database query or recommendation pipeline failed: {e}")
else:
    st.info("Please enter a decklist in the sidebar and click **Analyze & Recommend** to get started.")