"""In-memory record store with keyword search."""

from operator import itemgetter
from typing import Any, Dict, Iterator, List

from ant_common.search import keyword_filter


class KeywordStore:
    """Stores dict records and searches them by one text field."""

    def __init__(self, text_field: str = "text"):
        self.text_field = text_field
        self.entries: List[Dict[str, Any]] = []

    def add(self, text: Any, **fields: Any) -> Dict[str, Any]:
        """Append a record built from the searchable text plus extra fields."""
        entry = {self.text_field: text, **fields}
        self.entries.append(entry)
        return entry

    def search(self, query: str) -> List[Dict[str, Any]]:
        return keyword_filter(self.entries, query, key=itemgetter(self.text_field))

    def all(self) -> List[Dict[str, Any]]:
        return self.entries

    def clear(self) -> None:
        self.entries = []

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        return iter(self.entries)
