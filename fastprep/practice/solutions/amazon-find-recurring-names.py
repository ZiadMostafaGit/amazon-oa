# Hash-map counting of sorted-letter signatures (anagram keys) over allNames.
from typing import List, Optional, Any
from collections import Counter


def findRecurringNames(realNames: List[str], allNames: List[str]) -> List[str]:
    counts = Counter("".join(sorted(name)) for name in allNames)
    result = [name for name in realNames if counts.get("".join(sorted(name)), 0) >= 2]
    result = sorted(set(result))
    return result if result else ["None"]
