import urllib.parse

def get_card_image_url(card_name: str, db_image_url: str) -> str:
    """Returns db_image_url if valid; otherwise generates a dynamic Scryfall image link."""
    if db_image_url and isinstance(db_image_url, str) and db_image_url.strip():
        return db_image_url.strip()
    encoded_name = urllib.parse.quote(card_name)
    return f"https://api.scryfall.com/cards/named?exact={encoded_name}&format=image"