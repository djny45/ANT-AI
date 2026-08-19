"""Generic name to object registry."""

from typing import Dict, Generic, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """Keyed registry used by agent, connector, skill and provider registries."""

    def __init__(self) -> None:
        self._items: Dict[str, T] = {}

    @property
    def mapping(self) -> Dict[str, T]:
        """Live mapping of registered names to objects."""
        return self._items

    def register(self, name: str, item: T) -> None:
        self._items[name] = item

    def get(self, name: str) -> Optional[T]:
        return self._items.get(name)

    def remove(self, name: str) -> None:
        self._items.pop(name, None)

    def names(self) -> List[str]:
        return list(self._items.keys())

    def values(self) -> List[T]:
        return list(self._items.values())

    def clear(self) -> None:
        self._items = {}

    def __contains__(self, name: object) -> bool:
        return name in self._items

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[str]:
        return iter(self._items)
