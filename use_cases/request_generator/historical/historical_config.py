from datetime import datetime, timedelta


class HistoricalConfig:
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        interval: timedelta,
        go_back_in_time: bool = True,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.go_back_in_time = go_back_in_time
