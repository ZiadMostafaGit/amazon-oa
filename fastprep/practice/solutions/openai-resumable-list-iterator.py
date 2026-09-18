# Resumable iterator with an opaque state object; replay every saved state to exhaustion.
from typing import List, Optional, Any


class _ListIterator:
    """Finite iterator over a list whose progress can be saved/restored opaquely."""

    def __init__(self, values: List[int]) -> None:
        self._values = values
        self._pos = 0

    def has_next(self) -> bool:
        return self._pos < len(self._values)

    def next(self) -> int:
        if not self.has_next():
            raise StopIteration("iterator exhausted")
        value = self._values[self._pos]
        self._pos += 1
        return value

    def get_state(self) -> Any:
        # Opaque, serializable snapshot; callers must not inspect its shape.
        return {"consumed": self._pos}

    def set_state(self, state: Any) -> None:
        self._pos = state["consumed"]


def resumeSuffixes(values: List[int]) -> List[List[int]]:
    source = list(values)

    it = _ListIterator(source)
    saved: List[Any] = [it.get_state()]
    while it.has_next():
        it.next()
        saved.append(it.get_state())

    result: List[List[int]] = []
    for state in saved:
        fresh = _ListIterator(source)
        fresh.set_state(state)
        suffix: List[int] = []
        while fresh.has_next():
            suffix.append(fresh.next())
        result.append(suffix)
    return result
