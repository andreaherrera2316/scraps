from datetime import datetime, timedelta
from typing import Callable, Optional
from decorators.base_class import baseclass
from entities.scrape_request.dated_request import DatedRequest
from entities.scrape_request.scrape_request import ScrapeRequest
from use_cases.request_generator.historical.historical_config import HistoricalConfig
from use_cases.request_generator.request_generator import RequestGenerator
from formatters.ymd_formatter import ymd_format_date


class HistoricalRequestGenerator(RequestGenerator):
    """
    Essentially this class takes in a request template in the form of a [ScrapeRequest]
    It will extract the payload and url of that request, and copy it to a [DatedRequest]

    Based on the [HistoricalConfig] [start_date] and [end_date]
    It will create requests ranging between those two dates

    Every request will have a time difference of the defined [interval]
    By default the requests will be done from the [end_date -> start_date] defined by [go_back_in_time =True]
    """

    def __init__(
        self,
        config: HistoricalConfig,
        initial_request: ScrapeRequest,
        start_key: Optional[str] = "from",
        end_key: Optional[str] = "to",
        date_formatter: Callable[[datetime], str] = ymd_format_date,
    ):
        self.config = config
        self.initial_request = initial_request
        self.start_key = start_key
        self.end_key = end_key
        self.date_formatter: Callable[[datetime], str] = date_formatter
        self._requests_made: int = 0

        if config.go_back_in_time:
            self.current_start_date = config.end_date - config.interval
            self.current_end_date = config.end_date

        else:
            self.current_start_date = config.start_date
            self.current_end_date = config.start_date + config.interval

    @baseclass
    def working(self) -> bool:
        """
        Whether the generator has generated all the requests
        To gather all the info from [HistoricalConfig] [start_date] and [end_date]
        or not
        """
        return self._continue_generating() or self.has_remainder()

    @baseclass
    def next(self) -> Optional[DatedRequest]:
        """
        The next dated request to be done
        """
        if not self.working():
            return None

        if self._continue_generating():
            self._requests_made += 1
            return self._generate_interval_request()

        if self.has_remainder():
            self._requests_made += 1
            return self._generate_remainder_request()

    @baseclass
    def total_requests(self):
        return self._requests_made

    @baseclass
    def _continue_generating(self) -> bool:
        """
        Whether the generator has generated all the requests with the specified time interval
        """
        if self.config.go_back_in_time:
            return self.current_start_date >= self.config.start_date
        else:
            return self.current_end_date <= self.config.end_date

    def has_remainder(self) -> bool:
        """
        Checks if there is a remainder interval left.
        """
        if self.config.go_back_in_time:
            remainder = (
                self.current_start_date - self.config.start_date
            ) % self.config.interval
        else:
            remainder = (
                self.config.end_date - self.current_end_date
            ) % self.config.interval

        return remainder > timedelta(0)

    def _generate_interval_request(self) -> DatedRequest:
        """
        Generates the next request according to the time start, end and time interval config.
        """
        dated_request = DatedRequest(
            self.initial_request.url,
            self.initial_request.get_payload(),
            self.current_start_date,
            self.current_end_date,
            self.start_key,
            self.end_key,
            self.date_formatter,
        )

        # Update state for the next request by adding the interval
        # If the date  is out of the time range we are requesting
        # Then _continue_generating() will eval to false and working will terminate
        # Unless has_remainder() is true in which case one more request will be made
        if self.config.go_back_in_time:
            self.current_start_date -= self.config.interval
            self.current_end_date -= self.config.interval
        else:
            self.current_start_date += self.config.interval
            self.current_end_date += self.config.interval

        return dated_request

    def _generate_remainder_request(self) -> DatedRequest:
        """
        Generates a request for the remaining time interval.
        """
        if self.config.go_back_in_time:
            remainder_start = self.config.start_date
            remainder_end = (
                self.current_end_date
            )  # current_end_date is the start_date of the previous request
        else:
            remainder_start = (
                self.current_start_date
            )  # current_start_date is the end_date of the previous request
            remainder_end = self.config.end_date

        # Update the state to values out of the time range the gnerator is making requests,
        # in order to terminate execution, because remainder request should be the last request
        if self.config.go_back_in_time:
            self.current_start_date = self.config.start_date - self.config.interval
            self.current_end_date = self.current_start_date
        else:
            self.current_end_date = self.config.end_date + self.config.interval
            self.current_start_date = self.current_end_date

        return DatedRequest(
            self.initial_request.url,
            self.initial_request.get_payload(),
            remainder_start,
            remainder_end,
            self.start_key,
            self.end_key,
            self.date_formatter,
        )
