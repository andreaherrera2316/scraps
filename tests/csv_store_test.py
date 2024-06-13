import csv
import os
import shutil
from typing import List, Tuple
import unittest
from data.csv.csv_store import CSVStore
from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.scraped_data import ScrapedData
from tests.mocks.generate_request_data_pairs import generate_request_data_pairs


class TestCSVStore(unittest.TestCase):
    def setUp(self):
        # Test Stores
        self.csv_store_multiple_files = CSVStore(multiple_files=True)
        self.csv_store_single_file = CSVStore(multiple_files=False)

        # Test Data
        url = "https://example.com"
        payload = {"key": "value"}
        num_samples = 3
        num_keys = 4

        self.data_pairs_1: List[Tuple[ScrapeRequest, ScrapedData]] = (
            generate_request_data_pairs(url, payload, num_samples, num_keys)
        )

        url = "https://example.com/should/be/different/site/because/of/deep/links"
        payload = {"key": "value"}
        num_samples = 2
        num_keys = 3

        self.data_pairs_2: List[Tuple[ScrapeRequest, ScrapedData]] = (
            generate_request_data_pairs(url, payload, num_samples, num_keys)
        )

    def tearDown(self):
        folder = "example.com"
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def test_save_to_multiple_files(self):
        """
        Check to see if every sample was saved in a separate file
        """
        for sample in self.data_pairs_1:
            request: ScrapeRequest = sample[0]
            data: ScrapedData = sample[1]
            self.csv_store_multiple_files.save(data, request)

        folder = "example.com"
        files_in_folder: int = len(os.listdir(folder))
        expected_files: int = len(self.data_pairs_1)
        self.assertIs(expected_files, files_in_folder)

    def test_save_to_single_file(self):
        """
        Checks to see if all the samples were saved in a single file
        """
        for sample in self.data_pairs_1:
            request: ScrapeRequest = sample[0]
            data: ScrapedData = sample[1]
            self.csv_store_single_file.save(data, request)

        folder = "example.com"
        files_in_folder: int = len(os.listdir(folder))
        self.assertIs(1, files_in_folder)

    def test_multiple_files_and_multiple_urls(self):
        """
        Check to see if every sample from both data_pairs lists were saved each in a separate file
        and in the same folder (as they have the same base url)
        """
        for sample in self.data_pairs_1:
            request: ScrapeRequest = sample[0]
            data: ScrapedData = sample[1]
            self.csv_store_multiple_files.save(data, request)

        for sample in self.data_pairs_2:
            request: ScrapeRequest = sample[0]
            data: ScrapedData = sample[1]
            self.csv_store_multiple_files.save(data, request)

        folder = "example.com"
        files_in_folder: int = len(os.listdir(folder))
        expected_files: int = len(self.data_pairs_1) + len(self.data_pairs_2)
        self.assertIs(expected_files, files_in_folder)

    def test_single_files_and_multiple_urls(self):
        """
        Check to see if every sample from both data_pairs lists were saved in two separate file
        one file per each unique url, and in the same folder (as they have the same base url)
        """
        for sample in self.data_pairs_1:
            request: ScrapeRequest = sample[0]
            data: ScrapedData = sample[1]
            self.csv_store_single_file.save(data, request)

        for sample in self.data_pairs_2:
            request: ScrapeRequest = sample[0]
            data: ScrapedData = sample[1]
            self.csv_store_single_file.save(data, request)

        folder = "example.com"
        files_in_folder: int = len(os.listdir(folder))
        self.assertIs(2, files_in_folder)

    def test_data_saved_to_multiple_files(self):
        """
        Checks to see if the data was saved in it's respective file
        """
        for sample in self.data_pairs_1:
            request: ScrapeRequest = sample[0]
            data: ScrapedData = sample[1]
            self.csv_store_multiple_files.save(data, request)

        folder = "example.com"
        files_in_folder: List[str] = os.listdir(folder)

        # Sort the data pairs and files in the folder
        sorted_data_pairs = sorted(self.data_pairs_1, key=lambda x: x[0].url)
        sorted_files = sorted(files_in_folder)

        # Compare the sorted data pairs with the sorted files
        for i in range(len(sorted_files)):
            data = sorted_data_pairs[i]
            filename = sorted_files[i]
            self._check_data_in_csv_file(folder, filename, [data])

    def test_data_saved_to_single_file(self):
        """
        Checks to see if all the data samples are saved in a single file,
        """
        for sample in self.data_pairs_1:
            request: ScrapeRequest = sample[0]
            data: ScrapedData = sample[1]
            self.csv_store_single_file.save(data, request)
            
        folder = "example.com"
        filename: str = os.listdir(folder)[0]
        self._check_data_in_csv_file(folder, filename, self.data_pairs_1)

    # * Helper
    def _check_data_in_csv_file(
        self,
        folder: str,
        filename: str,
        data_pairs: List[Tuple[ScrapeRequest, ScrapedData]],
    ):
        file_path = os.path.join(folder, filename)
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                expected_data = data_pairs[i % len(data_pairs)][1].get_data()
                for key, expected_value in expected_data.items():
                    self.assertEqual(row[key], str(expected_value))


if __name__ == "__main__":
    unittest.main()
