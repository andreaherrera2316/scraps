from typing import Any, Dict, Optional
import unittest
from unittest.mock import AsyncMock, MagicMock
import asyncio

from data.data_store import DataStore
from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.factory.scrape_data_factory import ScrapeDataFactory
from entities.scraped_data.scraped_data import ScrapedData
from use_cases.request_generator.request_generator import RequestGenerator
from use_cases.scraper.scraper_config import ScraperConfig
from use_cases.scraper.tor.tor_scraper import TorScraper


# Mock classes
class MockScrapeRequest(ScrapeRequest):
    def __init__(self, url):
        self._url = url

    def url(self):
        return self._url


class MockScrapedData(ScrapedData):
    def __init__(self, data):
        self.data = data


class MockRequestGenerator(RequestGenerator):
    def __init__(self):
        self.requests = [MockScrapeRequest(f"http://example.com/{i}") for i in range(3)]
        self.index = 0

    def working(self) -> bool:
        return self.index < len(self.requests)

    def next(self) -> Optional[MockScrapeRequest]:
        if self.index < len(self.requests):
            request = self.requests[self.index]
            self.index += 1
            return request
        return None

    @property
    def total_requests(self) -> int:
        return len(self.requests)


class MockScrapeDataFactory(ScrapeDataFactory[MockScrapedData]):
    def create(self, data: Dict[str, Any]) -> MockScrapedData:
        return MockScrapedData(data)


class MockDataStore(DataStore):
    def save(self, data: ScrapedData, request: ScrapeRequest) -> None:
        print(f"Saved data: {data.data} from {request.url()}")


class TestTorScraper(unittest.TestCase):
    def setUp(self):
        self.request_generator = MockRequestGenerator()
        self.data_factory = MockScrapeDataFactory()
        self.data_store = MockDataStore()
        self.config = ScraperConfig(interval_start=0.1, interval_end=0.2)
        self.scraper = TorScraper(
            self.request_generator, self.data_factory, self.data_store, self.config
        )

        self.scraper.fetch = AsyncMock(
            side_effect=lambda req: {"content": f"data from {req.url()}"}
        )

    def test_scrape(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.scraper.scrape())

        self.assertEqual(self.request_generator.total_requests, 3)


if __name__ == "__main__":
    unittest.main()
