from typing import Any, Dict


class ScrapedData:

    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data

    def get_data(self) -> Dict[str, Any]:
        return self._data

    def get_value(self, key: str) -> Any | None:
        return self._data[key]

    def set_value(self, key: str, value: Any) -> None:
        self._data[key] = value
