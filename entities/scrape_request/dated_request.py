from datetime import datetime
from typing import Dict, Any

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
    ):
        super().__init__(url, payload)
        self._start_date = start_date
        self._end_date = end_date
        self.start_key = start_key
        self.end_key = end_key
        # Update Payload with ISO formatted dates without milliseconds and with 'Z' at the end
        payload[self.start_key] = (
            self._start_date.replace(microsecond=0).isoformat() + ".000Z"
        )
        payload[self.end_key] = (
            self._end_date.replace(microsecond=0).isoformat() + ".000Z"
        )
        self.payload = payload

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
