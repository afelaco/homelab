import polars as pl
import streamlit as st
from sqlalchemy import Engine, text


def render_synergies_admin_tab(engine: Engine):
    st.subheader("🔮 Synergy Matrix Management")
    st.markdown("Add, view, or remove tag synergy mappings in the database.")

    with engine.connect() as conn:
        # Fetch available tags for dropdowns
        tags_result = conn.execute(text("SELECT tag FROM dim_tags ORDER BY tag ASC;"))
        all_tags = [row[0] for row in tags_result.fetchall()]

        # Fetch current synergies
        syn_result = conn.execute(text("SELECT tag_a, tag_b FROM dim_synergies ORDER BY tag_a, tag_b ASC;"))
        synergies_df = pl.DataFrame(syn_result.fetchall(), schema=list(syn_result.keys()))

    # --- ADD NEW PAIR FORM ---
    with st.form("add_synergy_form", clear_on_submit=True):
        st.markdown("##### Add New Synergy Pair")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            tag_a = st.selectbox("Tag A", options=all_tags if all_tags else [""])
        with col2:
            tag_b = st.selectbox("Tag B", options=all_tags if all_tags else [""])
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("➕ Add Pair", type="primary")

        if submitted and tag_a and tag_b:
            try:
                with engine.begin() as conn:
                    # Insert both directions for full symmetry
                    conn.execute(
                        text(
                            "INSERT INTO dim_synergies (tag_a, tag_b) VALUES (:a, :b), (:b, :a) ON CONFLICT DO NOTHING;"
                        ),
                        {"a": tag_a, "b": tag_b},
                    )
                st.success(f"Added synergy pair: **{tag_a}** ⇄ **{tag_b}**")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to add synergy: {e}")

    st.markdown("---")
    st.markdown("##### Existing Synergy Pairs")

    if synergies_df.is_empty():
        st.info("No synergy pairs found in the database.")
        return

    # --- DISPLAY & DELETE INTERFACE ---
    synergies_pd = synergies_df.to_pandas()

    # Simple table view with delete action per row
    for idx, row in synergies_pd.iterrows():
        t_a, t_b = row["tag_a"], row["tag_b"]
        col_row_info, col_row_btn = st.columns([5, 1])

        with col_row_info:
            st.markdown(f"`{t_a}` ⇄ `{t_b}`")
        with col_row_btn:
            if st.button("🗑️ Delete", key=f"del_{t_a}_{t_b}_{idx}"):
                try:
                    with engine.begin() as conn:
                        conn.execute(
                            text(
                                "DELETE FROM dim_synergies WHERE (tag_a = :a AND tag_b = :b) OR (tag_a = :b AND tag_b = :a);"
                            ),
                            {"a": t_a, "b": t_b},
                        )
                    st.success(f"Removed synergy pair: {t_a} & {t_b}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete synergy: {e}")
