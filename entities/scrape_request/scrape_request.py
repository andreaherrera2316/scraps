from typing import Dict, Any


class ScrapeRequest:
    def __init__(self, url: str, payload: Dict[str, Any]):
        self.url = url
        self._payload = payload

    def set_payload(self, payload: Dict[str, Any]) -> None:
        self._payload = payload

    def get_payload(self) -> Dict[str, Any]:
        return self._payload
