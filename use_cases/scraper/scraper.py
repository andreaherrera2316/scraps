from abc import ABC, abstractmethod
import asyncio
import random
from typing import Any, Dict

from data.data_store import DataStore
from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.factory.scrape_data_factory import D, ScrapeDataFactory
from use_cases.request_generator.request_generator import RequestGenerator
from use_cases.scraper.scraper_config import ScraperConfig


class Scraper(ABC):
    def __init__(
        self,
        request_generator: RequestGenerator,
        data_factory: ScrapeDataFactory[D],
        data_store: DataStore,
        config: ScraperConfig,
    ):
        self.request_generator = request_generator
        self.data_factory = data_factory
        self.data_store = data_store
        self.config = config
        self.stop = False

    @abstractmethod
    async def fetch(self, request: ScrapeRequest) -> Dict[str, Any] | None:
        pass

    async def scrape(self) -> None:
        while self.request_generator.working() and not self.stop:
            request = self.request_generator.next()
            response = await self.fetch(request)
            if response is not None:
                data = self.data_factory.create(response)
                self.data_store.save(data, request)
                await asyncio.sleep(
                    random.uniform(self.config.interval_start, self.config.interval_end)
                )
