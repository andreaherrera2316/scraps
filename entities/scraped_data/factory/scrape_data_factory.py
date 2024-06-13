from abc import ABC, abstractmethod
from typing import Any, Dict, TypeVar, Generic

from entities.scraped_data.scraped_data import ScrapedData


D = TypeVar("D", bound=ScrapedData)


class ScrapeDataFactory(ABC, Generic[D]):
    """
    The factory is used by the [Scraper]
    It create a new object to store the data per every request it scraped
    The purpose of using a factory is to be flexible on the runtime type
    Allowing the creation of custom objects that will fit the data collected
    And optionally add additional capabilities, depeding on the data.

    Example: Scraping HTML data
    We might want to create an object HTMLData that will clean the tags
    and extract the data, streamlining some of the pre-processing.
    """

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> D:
        pass
