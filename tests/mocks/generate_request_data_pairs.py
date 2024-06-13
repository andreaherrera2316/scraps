from typing import Any, Dict, List, Tuple

from entities.scrape_request.scrape_request import ScrapeRequest
from entities.scraped_data.scraped_data import ScrapedData


def generate_request_data_pairs(
    url: str, payload: Dict[str, Any], num_samples: int, num_keys: int
) -> List[Tuple[ScrapeRequest, ScrapedData]]:
    pairs = []
    for i in range(num_samples):
        request = ScrapeRequest(url, payload)
        data = ScrapedData({f"key{j}": i for j in range(num_keys)})
        pairs.append((request, data))
    return pairs
