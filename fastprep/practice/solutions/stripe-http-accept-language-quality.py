# Greedy pass over header entries (exact, then generic prefix, then wildcard), then stable sort by quality desc.
from typing import List, Optional, Any


def parseAcceptLanguageWithQuality(acceptHeader: str, supportedLanguages: List[str]) -> List[str]:
    entries = []
    for raw in (acceptHeader or "").split(","):
        part = raw.strip()
        if not part:
            continue
        pieces = part.split(";")
        tag = pieces[0].strip()
        if not tag:
            continue
        q = 1.0
        for extra in pieces[1:]:
            extra = extra.strip()
            if extra.lower().startswith("q="):
                try:
                    q = float(extra[2:].strip())
                except ValueError:
                    q = 1.0
        entries.append((tag, q))

    lowered = [s.lower() for s in supportedLanguages]
    used = [False] * len(supportedLanguages)
    matched = []  # (quality, index in match order, tag)

    for tag, q in entries:
        low = tag.lower()
        if low == "*":
            for i, s in enumerate(lowered):
                if not used[i]:
                    used[i] = True
                    matched.append((q, supportedLanguages[i]))
            continue
        hit = False
        for i, s in enumerate(lowered):
            if not used[i] and s == low:
                used[i] = True
                matched.append((q, supportedLanguages[i]))
                hit = True
        if hit:
            continue
        prefix = low + "-"
        for i, s in enumerate(lowered):
            if not used[i] and s.startswith(prefix):
                used[i] = True
                matched.append((q, supportedLanguages[i]))

    matched.sort(key=lambda item: -item[0])
    return [tag for _, tag in matched]
