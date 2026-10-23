import polars as pl
from pathlib import Path
import re
import homelab.core.dataset.bronze.google_drive
import homelab.core.endpoint.google_drive
from homelab import SETTINGS
from homelab.extract.google_drive import ExtractGoogleDrive


class ExtractGoogleDriveDecks(ExtractGoogleDrive):
    def __init__(self) -> None:
        super().__init__(
            endpoint=homelab.core.endpoint.google_drive.files,
            dataset=homelab.core.dataset.bronze.google_drive.decks,
        )

    def get_data(self) -> pl.DataFrame:
        input_path = Path(f"{SETTINGS.ROOT}/data/input")
        dfs = []

        for file_path in input_path.glob("*.txt"):
            df = self.parse_decklist_file(file_path)
            dfs.append(df)

        return pl.concat(dfs)

    @staticmethod
    def parse_decklist_file(file_path: Path) -> pl.DataFrame:
        deck_name = file_path.stem
        pattern = re.compile(r"^(\d+)\s+(.+)$")

        records = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or line_str.startswith("["):
                    continue

                match = pattern.match(line_str)
                if match:
                    copies = int(match.group(1))
                    card_name = match.group(2).strip()
                    records.append({"deck": deck_name, "card": card_name, "copies": copies})

        return pl.DataFrame(records)


if __name__ == "__main__":
    ExtractGoogleDriveDecks().run()
