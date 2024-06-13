import unittest
from datetime import datetime, timedelta
from entities.scrape_request.scrape_request import ScrapeRequest
from use_cases.request_generator.historical.historical_config import HistoricalConfig
from use_cases.request_generator.historical.historical_request_generator import (
    HistoricalRequestGenerator,
)


class TestHistoricalRequestGenerator(unittest.TestCase):
    def setUp(self):
        self.url = "https://example.com/api"
        self.payload = {"param": "value"}
        self.start_date = datetime(2024, 1, 1)
        self.end_date = datetime(2024, 1, 7)
        self.interval = timedelta(days=1)
        self.initial_request = ScrapeRequest(self.url, self.payload)
        self.config = HistoricalConfig(
            start_date=self.start_date,
            end_date=self.end_date,
            interval=self.interval,
            go_back_in_time=False,
        )

    def test_request_generation_forward(self):
        generator = HistoricalRequestGenerator(self.config, self.initial_request)
        requests = []
        print("GEN FORWARD")

        while generator.working():
            request = generator.next()
            requests.append(request)
            print(
                f"Generating request: start_date={request.start_date}, end_date={request.end_date}"
            )
        self.assertEqual(len(requests), 6)

    def test_request_generation_backward(self):
        print("GEN BACKWARD")
        config = HistoricalConfig(
            start_date=self.start_date,
            end_date=self.end_date,
            interval=self.interval,
            go_back_in_time=True,
        )
        generator = HistoricalRequestGenerator(config, self.initial_request)
        requests = []
        while generator.working():
            request = generator.next()
            requests.append(request)
            print(
                f"Generating request: start_date={request.start_date}, end_date={request.end_date}"
            )
        self.assertEqual(len(requests), 6)

    def test_has_remainder_true(self):
        config = HistoricalConfig(
            start_date=self.end_date,
            end_date=self.end_date + timedelta(hours=1),
            interval=self.interval,
            go_back_in_time=False,
        )
        generator = HistoricalRequestGenerator(config, self.initial_request)
        self.assertIs(generator.has_remainder(), True)

    def test_has_remainder_false(self):
        config = HistoricalConfig(
            start_date=self.end_date,
            end_date=self.end_date,
            interval=self.interval,
            go_back_in_time=False,
        )
        generator = HistoricalRequestGenerator(config, self.initial_request)
        self.assertIs(generator.has_remainder(), False)

    def test_forward_has_remainder_true_after_request_false(self):
        config = HistoricalConfig(
            start_date=self.end_date,
            end_date=self.end_date + timedelta(hours=1),
            interval=self.interval,
            go_back_in_time=False,
        )
        generator = HistoricalRequestGenerator(config, self.initial_request)
        self.assertIs(generator.has_remainder(), True)
        request = generator.next()
        self.assertIs(generator.has_remainder(), False)

    def test_backward_has_remainder_true_after_request_false(self):
        config = HistoricalConfig(
            start_date=self.end_date,
            end_date=self.end_date + timedelta(hours=1),
            interval=self.interval,
            go_back_in_time=False,
        )
        generator = HistoricalRequestGenerator(config, self.initial_request)
        self.assertIs(generator.has_remainder(), True)
        request = generator.next()
        self.assertIs(generator.has_remainder(), False)

    def test_request_generation_custom_interval(self):
        interval = timedelta(hours=1)
        config = HistoricalConfig(
            start_date=self.start_date, end_date=self.end_date, interval=interval
        )
        generator = HistoricalRequestGenerator(config, self.initial_request)
        requests = []
        while generator.working():
            requests.append(generator.next())
        self.assertEqual(len(requests), 6 * 24)  # 6 days * 24 hours per day

    def test_request_generation_forward_with_remainder(self):
        print("\nFORWARD REMAINDER:")
        config = HistoricalConfig(
            start_date=self.start_date,
            end_date=self.end_date + timedelta(hours=1),
            interval=self.interval,
            go_back_in_time=False,
        )

        generator = HistoricalRequestGenerator(config, self.initial_request)

        requests = []
        while generator.working():
            request = generator.next()
            requests.append(request)
            print(
                f"Generating request: start_date={request.start_date}, end_date={request.end_date}"
            )
        self.assertEqual(len(requests), 7)

    def test_request_generation_backward_with_remainder(self):
        print("\nBACKWARD REMAINDER:")
        config = HistoricalConfig(
            start_date=self.start_date,
            end_date=self.end_date + timedelta(hours=1),
            interval=self.interval,
            go_back_in_time=True,
        )
        generator = HistoricalRequestGenerator(config, self.initial_request)
        self.assertIs(generator.has_remainder(), True)
        requests = []
        while generator.working():
            request = generator.next()
            requests.append(request)
            print(
                f"Generating request: start_date={request.start_date}, end_date={request.end_date}"
            )
        self.assertEqual(len(requests), 7)


if __name__ == "__main__":
    unittest.main()
