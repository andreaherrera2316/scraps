import asyncio
from typing import Any, Dict
import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector
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
            "socks5://127.0.0.1:9050",  # Default Tor proxy
            # "socks5://127.0.0.1:9150",  # Tor Browser default proxy
            # "socks5://127.0.0.1:9250",  # Custom proxy if available
        ]

    @baseclass
    async def fetch(self, request: ScrapeRequest) -> Dict[str, Any]:

        # Implement logic to route the request via the Tor network
        response = None
        proxies = len(self.tor_proxies)
        for _ in range(proxies):
            response = await self.__fetch_with_proxy(request)
            if response:
                break
            await asyncio.sleep(2)  # Wait between Tor network reroutes
        return response

    async def __fetch_with_proxy(self, request: ScrapeRequest) -> Dict[str, Any] | None:
        proxy_url = random.choice(self.tor_proxies)
        proxy = ProxyConnector.from_url(proxy_url)
        headers = self.__generate_headers()
        async with aiohttp.ClientSession(connector=proxy, headers=headers) as session:
            async with session.get(
                request.url, params=request.get_payload()
            ) as response:
                print("RESPONSE")
                print(f"URL: {request.url}")
                print(f"PAYLOAD: {request.get_payload()}")
                print(f"TYPE: {response.content_type}")
                content = await response.text()
                print(f"CONTENT: {content}")
                return await self.__handle_response_status(response)

    async def __handle_response_status(self, response) -> Dict[str, Any] | None:
        if response.status >= 200 and response.status < 300:  # Got Data
            return await response.json()
        elif response.status == 403:  # FORBIDDEN
            print("We've been made! RETREAT")
            self.stop = True
            return None
        else:
            print(f"Unexpected response: {response.status}")
            return None

    def __generate_headers(self) -> Dict[str, str]:
        user_agent = self.__generate_user_agent()
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }
        return headers

    def __generate_user_agent(self) -> str:
        # Generate a random bogus User-Agent
        browsers = ["Mozilla", "Chrome", "Opera", "Safari", "Edge"]
        operating_systems = [
            "Windows NT 10.0; Win64; x64",
            "Linux x86_64",
            "Macintosh; Intel Mac OS X 10_15_7",
        ]
        browser = random.choice(browsers)
        os = random.choice(operating_systems)
        version = random.randint(60, 99)
        return f"{browser}/{version}.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0 Safari/537.36"
