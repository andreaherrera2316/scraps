from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from entities.scrape_request.scrape_request import ScrapeRequest

T = TypeVar("T", bound=ScrapeRequest)


class RequestGenerator(ABC):
    """
    Blueprint to create a class in charge of generating scrape requests,
    that will keep track of what request should be done next and generate it
    """

    @abstractmethod
    def working(self) -> bool:
        """
        Whether the generator is actively generating requests or it's done.
        """
        pass

    @abstractmethod
    def next(self) -> Optional[T]:
        """
        The next scrape request, if any.
        """
        pass

    @property
    @abstractmethod
    def total_requests(self):
        """
        The amount of requests that have been generated.
        """
        pass
