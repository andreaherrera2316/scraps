import requests
from typing import Any, Dict

from data.data_store import DataStore
from decorators.base_class import baseclass
from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.factory.scrape_data_factory import D, ScrapeDataFactory
from use_cases.request_generator.request_generator import RequestGenerator
from use_cases.scraper.scraper import Scraper
from use_cases.scraper.scraper_config import ScraperConfig


class RegularScraper(Scraper):
    def __init__(
        self,
        request_generator: RequestGenerator,
        data_factory: ScrapeDataFactory[D],
        data_store: DataStore,
        config: ScraperConfig,
    ):
        super().__init__(request_generator, data_factory, data_store, config)

    @baseclass
    async def fetch(self, request: ScrapeRequest) -> Dict[str, Any]:
        response = requests.get(request.url, request.get_payload())
        print(response.content)
        return response.json()
