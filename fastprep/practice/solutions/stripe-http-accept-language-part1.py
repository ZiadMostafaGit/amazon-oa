# Scan header entries in order; match exact, generic prefix, or wildcard while deduping.
from typing import List, Optional, Any


def parseAcceptLanguage(acceptHeader: str, supportedLanguages: List[str]) -> List[str]:
    result = []
    used = set()

    entries = [p.strip() for p in (acceptHeader or "").split(",")]
    for tag in entries:
        if not tag:
            continue
        low = tag.lower()
        for idx, sup in enumerate(supportedLanguages):
            if idx in used:
                continue
            s = sup.lower()
            if low == "*" or s == low or s.startswith(low + "-"):
                used.add(idx)
                result.append(sup)
    return result
