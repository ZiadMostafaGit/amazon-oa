# Hash-map counting: compare per-name initiated vs completed counts, then sort the mismatches.
from typing import List, Optional, Any
from collections import Counter


def findBrokenCustomers(initiatedCustomers: List[str], completedCustomers: List[str]) -> List[str]:
    a = Counter(initiatedCustomers)
    b = Counter(completedCustomers)
    broken = [name for name in set(a) | set(b) if a[name] != b[name]]
    broken.sort()
    return broken
