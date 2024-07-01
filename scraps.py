import asyncio
from datetime import datetime, timedelta
from data.csv.csv_store import CSVStore
from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.factory.basic_data_factory import BasicDataFactory
from entities.scraped_data.factory.scrape_data_factory import ScrapeDataFactory
from entities.scraped_data.scraped_data import ScrapedData
from use_cases.request_generator.historical.historical_config import HistoricalConfig
from use_cases.request_generator.historical.historical_request_generator import (
    HistoricalRequestGenerator,
)
from use_cases.scraper.scraper_config import ScraperConfig
from use_cases.scraper.tor.tor_scraper import TorScraper
from use_cases.scraper.regular.regular_scraper import RegularScraper


class Scraps:
    def __init__(
        self,
        url: str,
        payload: dict,
        formatter,
        interval: timedelta,
        start: datetime,
        end: datetime,
        start_key: str,
        end_key: str,
        tor: bool,
        back_in_time=False,
        multiple_files=False,
    ):
        self.url = url
        self.payload = payload
        self.formatter = formatter
        self.interval = interval
        self.start = start
        self.end = end
        self.start_key = start_key
        self.end_key = end_key
        self.tor = tor
        self.back_in_time = back_in_time
        self.multiple_files = multiple_files

    def run(self):

        config_generator = HistoricalConfig(
            start_date=self.start,
            end_date=self.end,
            interval=self.interval,
            go_back_in_time=self.back_in_time,
        )
        historic_generator = HistoricalRequestGenerator(
            config=config_generator,
            initial_request=ScrapeRequest(self.url, self.payload),
            start_key=self.start_key,
            end_key=self.end_key,
            date_formatter=self.formatter,
        )

        # Data Factory
        basic_factory = BasicDataFactory({ScrapeDataFactory, ScrapedData})

        # Data Store
        csv_store = CSVStore(multiple_files=self.multiple_files)

        # Scraper
        config = ScraperConfig(3, 5)
        if self.tor:
            scraper = TorScraper(
                request_generator=historic_generator,
                data_factory=basic_factory,
                data_store=csv_store,
                config=config,
            )
        else:
            scraper = RegularScraper(
                request_generator=historic_generator,
                data_factory=basic_factory,
                data_store=csv_store,
                config=config,
            )

        print("Begin Scraping")
        asyncio.run(scraper.scrape())
        print("Done Scraping")
