# Simulate attempts in order with a strict hand-written recursive-descent/regex parser for the closed JSON grammar.
import re
from typing import List, Optional, Any

_OBJ = re.compile(r'^\{(?:"[A-Za-z0-9_-]+":"[A-Za-z0-9_-]*"(?:,"[A-Za-z0-9_-]+":"[A-Za-z0-9_-]*")*)?\}$')
_PAIR = re.compile(r'"([A-Za-z0-9_-]+)":"([A-Za-z0-9_-]*)"')


def _parse(body: str) -> Optional[List[Any]]:
    if _OBJ.match(body) is None:
        return None
    pairs = _PAIR.findall(body)
    keys = [k for k, _ in pairs]
    if len(set(keys)) != len(keys):
        return None
    return pairs


def handleResponses(statuses: List[int], bodies: List[str], maxAttempts: int) -> str:
    limit = min(maxAttempts, len(statuses))
    for i in range(limit):
        code = statuses[i]
        if 200 <= code <= 299:
            pairs = _parse(bodies[i])
            if pairs is None:
                return "JSON_ERROR"
            pairs.sort(key=lambda kv: kv[0])
            inner = ",".join('"%s":"%s"' % (k, v) for k, v in pairs)
            return "SUCCESS:{" + inner + "}"
        if code == 429 or 500 <= code <= 599:
            continue
        return "HTTP_%d" % code
    return "EXHAUSTED"
