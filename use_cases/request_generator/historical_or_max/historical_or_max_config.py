from datetime import datetime, timedelta

from use_cases.request_generator.historical.historical_config import HistoricalConfig


class HistoricalOrMaxConfig(HistoricalConfig):
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        interval: timedelta,
        max_requests: int,
        go_back_in_time: bool = True,
    ):
        super().__init__(start_date, end_date, interval, go_back_in_time)
        self.max_requests = max_requests
