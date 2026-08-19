"""Case-insensitive substring search helpers."""

from typing import Any, Callable, Iterable, List, Optional


def keyword_match(value: Any, query: str) -> bool:
    """Return True when query occurs in value, ignoring case."""
    return query.lower() in str(value).lower()


def keyword_filter(
    items: Iterable[Any],
    query: str,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """Return items whose text representation contains query.

    `key` extracts the searchable value from each item.
    """
    return [item for item in items if keyword_match(key(item) if key else item, query)]
