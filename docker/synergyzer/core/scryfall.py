import urllib.parse
import pandas as pd


def get_card_image_url(card_name: str, db_image_url) -> str:
    """Returns a valid image URL for single-faced and double-faced (MDFC) cards."""
    # Check if database provided a valid string URL
    if db_image_url is not None and not (isinstance(db_image_url, float) and pd.isna(db_image_url)):
        url_str = str(db_image_url).strip()
        if url_str and url_str.lower() != "nan" and url_str.lower() != "none":
            return url_str

    # If MDFC (contains '//'), extract front face name (e.g., 'Turntimber Symbiosis')
    clean_name = str(card_name).split("//")[0].strip()
    encoded_name = urllib.parse.quote(clean_name)

    return f"https://api.scryfall.com/cards/named?exact={encoded_name}&format=image"