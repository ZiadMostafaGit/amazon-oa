# Reduce-based helpers: map, filter and sum are each a single linear fold over the sequence.
from typing import List, Optional, Any


def _reduce(seq, fn, initial):
    acc = initial
    for item in seq:
        acc = fn(acc, item)
    return acc


def _append(acc, value):
    acc.append(value)
    return acc


def functionalStages(values: List[int], multiplier: int, minimum: int) -> List[List[int]]:
    mapped = _reduce(values, lambda acc, v: _append(acc, v * multiplier), [])
    filtered = _reduce(mapped, lambda acc, v: _append(acc, v) if v >= minimum else acc, [])
    total = _reduce(filtered, lambda acc, v: acc + v, 0)
    return [mapped, filtered, [total]]
