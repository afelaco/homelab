from homeauto.core.scraper.completionist_me import CompletionistMeScraper


class ExtractCompletionistMe:
    @property
    def scraper(self) -> CompletionistMeScraper:
        return CompletionistMeScraper()
