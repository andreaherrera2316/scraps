import csv
import os
from typing import Dict
from urllib.parse import urlparse
from data.data_store import DataStore
from decorators.base_class import baseclass
from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.scraped_data import ScrapedData


class CSVStore(DataStore):
    """
    DataStore implementation that will save the files in a CSV fromat
    """

    def __init__(self, multiple_files: bool = False):
        """
        If multiple_files=False [CSVStore] will group the data of requests from the same site into single csv
        If multiple_files=True [CSVStore] will cerate a new csv for the requests data
        """
        self.multiple_files = multiple_files
        self.urls_saved: Dict[str, int] = {}  # { "site.com": 1 }

    @baseclass
    def save(self, data: ScrapedData, request: ScrapeRequest) -> None:
        """
        Save the data scraped from the request
        """
        folder = self._get_folder(request.url)
        filename = self._get_filename(request.url)

        self._save_to(folder, filename, data)
        self._register_request(data, request)

    def _save_to(self, folder: str, filename: str, data: ScrapedData):
        """
        It uses the folder and filename to define the path where the data will be saved
        """
        file_path = os.path.join(folder, filename)

        # Open file in append mode
        with open(file_path, "a", newline="", encoding="utf-8") as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=data.get_data().keys())

            # If it's empty write the header row using the headers in the subsequent writewrow
            file_is_empty = os.path.getsize(file_path) == 0
            if file_is_empty:
                writer.writeheader()

            # Write data to CSV file
            writer.writerow(data.get_data())

    def _get_folder(self, url: str) -> str:
        """
        It will extract the base_url from the url
        And create a folder if one does not already exist in the cwd
        """
        parsed_url = urlparse(url)
        base_url = parsed_url.netloc

        # Create the folder if it doesn't exist
        folder_path = os.path.join(os.getcwd(), base_url)
        os.makedirs(folder_path, exist_ok=True)

        return folder_path

    def _get_filename(self, url: str) -> str:
        """
        Returns the file where the data should be saved
        If [multiple_files = True] it will return a new filename for the request
        If [multiple_files = False] it will return the name of the shared file for the url data
        """
        if self.multiple_files:
            return f"{ self._request_num_for_url(url) }_{ self._url_filename(url) }.csv"
        else:
            return f"{ self._url_filename(url) }.csv"

    def _url_filename(self, url: str) -> str:
        """
        Returns the url formatted to be saved as a file
        """
        return url.replace("https://", "").replace("/", "_")

    def _request_num_for_url(self, url: str) -> int:
        """
        Return the number of requests made for a url
        """
        num = self.urls_saved.get(url, 0)
        return num

    def _register_request(self, data: ScrapedData, request: ScrapeRequest):
        """
        Registers the request was made, for the specified url
        Keeps track of how many requests have been made for that url
        """
        current_num = self._request_num_for_url(request.url)
        self.urls_saved[request.url] = current_num + 1
