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
        self.start_date = start_date
        self.end_date = end_date
        self.start_key = start_key
        self.end_key = end_key

    def set_start_date(self, start_date: datetime) -> None:
        self.start_date = start_date
        self._update_payload()

    def set_end_date(self, end_date: datetime) -> None:
        self.end_date = end_date
        self._update_payload()
