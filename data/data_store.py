from abc import ABC, abstractmethod
from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.scraped_data import ScrapedData


class DataStore(ABC):
    """
    Blueprint to build a class that will store the data from a [ScrapeRequest]
    """

    @abstractmethod
    def save(self, data: ScrapedData, request: ScrapeRequest) -> None:
        pass
