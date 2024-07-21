from use_cases.request_generator.historical.historical_request_generator import (
    HistoricalRequestGenerator,
)


class HistoricalOrMaxRequestGenerator(HistoricalRequestGenerator):
    def working(self) -> bool:
        return self._requests_made < self.config.max_requests and super().working()
