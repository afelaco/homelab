from time import sleep

import requests
from bs4 import BeautifulSoup


class CompletionistMeScraper:
    def find_next(self, app_id: str) -> dict[str, str | None]:
        html = self.get(app_id)
        soup = BeautifulSoup(html, "html.parser")

        return {
            "app_id": app_id,
            **self.parse_fields(soup),
        }

    def get(self, app_id: str) -> str:
        url = self.get_url(app_id)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(
            url=url,
            headers=headers,
        )
        sleep(1)
        return response.text

    @staticmethod
    def get_url(app_id: str) -> str:
        return f"https://completionist.me/steam/app/{app_id}"

    def parse_fields(self, soup: BeautifulSoup) -> dict[str, str | None]:
        return {
            "completion_playtime_avg": self.find_element(soup, field="Completion Playtime Avg."),
            # Add more fields here later:
            # "percent_complete": self.extract_percent_complete(soup),
            # "total_achievements": self.extract_total_achievements(soup),
            # etc...
        }

    @staticmethod
    def find_element(soup: BeautifulSoup, field: str) -> str | None:
        label = soup.find(element=field)
        if not label:
            return None
        value = label.find_next()
        return value.text.strip() if value else None
