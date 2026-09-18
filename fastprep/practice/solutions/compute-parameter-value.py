# Ordered dict merge: later sources overwrite values, key order stays as first encountered.
from typing import List, Optional, Any


def computeParameterValue(sources: List[List[str]]) -> List[str]:
    final = {}
    for source in sources:
        for entry in source:
            key, _, value = entry.partition(":")
            final[key] = value
    return list(final.values())
