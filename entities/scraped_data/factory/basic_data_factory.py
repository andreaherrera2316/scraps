from typing import Any, Dict, TypeVar

from decorators.base_class import baseclass
from entities.scraped_data.factory.scrape_data_factory import ScrapeDataFactory
from entities.scraped_data.scraped_data import ScrapedData


D = TypeVar("D", bound=ScrapedData)


class BasicDataFactory(ScrapeDataFactory, ScrapedData):

    @baseclass
    def create(self, data: Dict[str, Any]) -> D:
        return ScrapedData(data)
