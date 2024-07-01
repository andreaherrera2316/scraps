from datetime import datetime
from typing import Dict, Any, Callable

from entities.scrape_request.scrape_request import ScrapeRequest


class DatedRequest(ScrapeRequest):
    def __init__(
        self,
        url: str,
        payload: Dict[str, Any],
        start_date: datetime,
        end_date: datetime,
        start_key: str = "from",
        end_key: str = "to",
        date_formatter: Callable[[datetime], str] = None,
    ):
        super().__init__(url, payload)
        self._start_date = start_date
        self._end_date = end_date
        self.start_key = start_key
        self.end_key = end_key
        self.date_formatter = date_formatter or self._default_date_formatter
        # Update Payload with formatted dates
        payload[self.start_key] = self.date_formatter(self._start_date)
        payload[self.end_key] = self.date_formatter(self._end_date)
        self.payload = payload

    @staticmethod
    def _default_date_formatter(date: datetime) -> str:
        return date.replace(microsecond=0).isoformat() + ".000Z"

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @start_date.setter
    def start_date(self, value: datetime) -> None:
        self._start_date = value
        self._update_payload()

    @property
    def end_date(self) -> datetime:
        return self._end_date

    @end_date.setter
    def end_date(self, value: datetime) -> None:
        self._end_date = value
        self._update_payload()

    def _update_payload(self) -> None:
        self.payload[self.start_key] = self.date_formatter(self._start_date)
        self.payload[self.end_key] = self.date_formatter(self._end_date)
