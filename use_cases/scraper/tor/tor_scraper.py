import asyncio
from typing import Any, Dict
import aiohttp
import random

from data.data_store import DataStore
from decorators.base_class import baseclass
from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.factory.scrape_data_factory import D, ScrapeDataFactory
from use_cases.request_generator.request_generator import RequestGenerator
from use_cases.scraper.scraper import Scraper
from use_cases.scraper.scraper_config import ScraperConfig


class TorScraper(Scraper):
    def __init__(
        self,
        request_generator: RequestGenerator,
        data_factory: ScrapeDataFactory[D],
        data_store: DataStore,
        config: ScraperConfig,
    ):
        super().__init__(request_generator, data_factory, data_store, config)
        self.tor_proxies = [
            "socks5h://127.0.0.1:9050",  # Default Tor proxy
            "socks5h://127.0.0.1:9150",  # Tor Browser default proxy
            "socks5h://127.0.0.1:9250",  # Custom proxy if available
        ]

    @baseclass
    async def fetch(self, request: ScrapeRequest) -> Dict[str, Any]:
        async def fetch_with_proxy(url: str) -> Dict[str, Any]:
            proxy = random.choice(self.tor_proxies)
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy) as response:
                    return await response.json()

        # Implement logic to route the request via the Tor network
        response = None
        for _ in range(3):
            response = await fetch_with_proxy(request.url())
            if response:
                break
            await asyncio.sleep(2)  # Wait between Tor network reroutes
        return response
