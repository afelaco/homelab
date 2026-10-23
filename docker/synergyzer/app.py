import streamlit as st
from config import get_engine
from core.parser import parse_manabox_text
from engine.recommender import run_recommendation_pipeline
from components.tab_summary import render_summary_tab
from components.tab_recommendations import render_recommendations_tab

st.set_page_config(
    page_title="Magic: The Gathering - Synergyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global SaaS-grade Styling, App-mode Framing, & Fantasy Typography
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hide the top-right Deploy button */
    [data-testid="stAppDeployButton"],
    .stAppDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* Make top header background transparent so sidebar toggle button remains visible & clickable */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 99999 !important;
    }

    /* Force the sidebar collapse/expand toggle button to stay visible in top-left */
    button[data-testid="stSidebarCollapseButton"],
    button[aria-label="Toggle sidebar"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        color: #ffffff !important;
        z-index: 100000 !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Apply fantasy serif font to body text */
    html, body, [class*="css"] {
        font-family: 'Lora', serif;
    }

    /* Apply majestic fantasy font to headers and titles */
    h1, h2, h3, h4, h5, h6, .stSubheader {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.5px;
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
        font-family: 'Lora', serif;
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