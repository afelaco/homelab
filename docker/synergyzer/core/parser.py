import re

import polars as pl


def parse_manabox_text(text: str) -> pl.DataFrame:
    """Parses raw text box input using a strict regex pattern and skips category headers."""
    pattern = re.compile(r"^(\d+)\s+(.+)$")
    records = []

    for line in text.strip().splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("["):
            continue

        match = pattern.match(line_str)
        if match:
            copies = int(match.group(1))
            card_name = match.group(2).strip()
            records.append({"quantity": copies, "card_name": card_name})

    if not records:
        return pl.DataFrame(schema={"quantity": pl.Int64, "card_name": pl.Utf8})
    return pl.DataFrame(records)
