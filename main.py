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


# Scrape Site Info
url = "https://example.com"
payload = {
    "static": "data",
}
request_sample = ScrapeRequest(url, payload)

# Generator
start = datetime.now() - timedelta(days=30) + timedelta(hours=23)
end = datetime.now() + timedelta(days=7, hours=22)
interval = timedelta(days=7)

config_generator = HistoricalConfig(start_date=start, end_date=end, interval=interval)
historic_generator = HistoricalRequestGenerator(
    config=config_generator,
    initial_request=request_sample,
    start_key="from",
    end_key="to",
)

# Data Factory
basic_factory = BasicDataFactory({ScrapeDataFactory, ScrapedData})

# Data Store
csv_store = CSVStore(multiple_files=False)

# Scraper
config = ScraperConfig(3, 5)
tor_scraper = TorScraper(
    request_generator=historic_generator,
    data_factory=basic_factory,
    data_store=csv_store,
    config=config,
)
regular_scraper = RegularScraper(
    request_generator=historic_generator,
    data_factory=basic_factory,
    data_store=csv_store,
    config=config,
)


print("Begin Scraping")
# asyncio.run(tor_scraper.scrape())
# asyncio.run(regular_scraper.scrape())
print("Done Scraping")
