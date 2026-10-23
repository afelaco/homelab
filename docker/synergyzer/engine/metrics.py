import polars as pl

RAMP_DRAW_KEYWORDS = {"ramp", "mana-producer", "card-draw", "draw", "cantrip", "accelerant", "fixer"}

def calculate_amv(deck_full_df: pl.DataFrame) -> float:
    """Calculates non-land Average Mana Value (AMV)."""
    non_land_df = deck_full_df.filter(~pl.col("type").str.contains("(?i)land"))
    if non_land_df.is_empty():
        return 0.0
    total_cmc = non_land_df.select((pl.col("cmc").fill_null(0) * pl.col("quantity")).sum()).item()
    total_count = non_land_df.select(pl.col("quantity").sum()).item()
    return total_cmc / total_count if total_count > 0 else 0.0

def calculate_actual_lands(deck_full_df: pl.DataFrame) -> int:
    """Counts total land cards in the deck."""
    land_df = deck_full_df.filter(pl.col("type").str.contains("(?i)land"))
    return int(land_df.select(pl.col("quantity").sum()).item()) if not land_df.is_empty() else 0

def detect_cheap_ramp_draw(deck_full_df: pl.DataFrame) -> int:
    """Counts non-land cards with CMC <= 2 tagged with ramp/draw/cantrip."""
    ramp_cards_df = deck_full_df.filter(
        (pl.col("cmc").fill_null(99) <= 2) &
        (~pl.col("type").str.contains("(?i)land")) &
        (pl.col("tags").list.eval(pl.element().str.to_lowercase().is_in(list(RAMP_DRAW_KEYWORDS))).list.any())
    )
    return int(ramp_cards_df.select(pl.col("quantity").sum()).item()) if not ramp_cards_df.is_empty() else 0

def calculate_karsten_lands(
    amv: float,
    n_ramp_draw: int,
    n_untapped_mdfc: float = 0.0,
    n_tapped_mdfc: float = 0.0,
    companion_c: int = 0
) -> float:
    """Computes Frank Karsten's linear regression model for baseline land requirements."""
    return 19.59 + (1.90 * amv) - (0.28 * n_ramp_draw) + (0.27 * companion_c) - (0.74 * n_untapped_mdfc) - (0.38 * n_tapped_mdfc)

def check_interaction_floor(deck_full_df: pl.DataFrame) -> tuple[int, str]:
    """Audits the maindeck for instant-speed interaction slots against the 7-slot floor."""
    interaction_df = deck_full_df.filter(pl.col("type").str.contains("(?i)instant"))
    count = int(interaction_df.select(pl.col("quantity").sum()).item()) if not interaction_df.is_empty() else 0
    status = "✅ Met (>= 7)" if count >= 7 else "⚠️ Below 7-Slot Floor"
    return count, status