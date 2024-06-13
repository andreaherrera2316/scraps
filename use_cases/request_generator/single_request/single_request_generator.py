from typing import Optional
from entities.scrape_request.scrape_request import ScrapeRequest
from use_cases.request_generator.request_generator import RequestGenerator


class SingleRequestGenerator(RequestGenerator):
    def __init__(self, initial_request: ScrapeRequest):
        self.initial_request = initial_request
        self.request_generated = False

    def working(self) -> bool:
        """
        Whether the generator is actively generating requests or it's done.
        The generator is working until the request has been generated and returned
        """
        return not self.request_generated

    def next(self) -> Optional[ScrapeRequest]:
        """
        The next scrape request, if any.
        """
        if self.working():
            self.request_generated = True
            return self.initial_request
        return None

    @property
    def total_requests(self) -> int:
        """
        The amount of requests that have been generated.
        """
        return 1 if self.request_generated else 0
