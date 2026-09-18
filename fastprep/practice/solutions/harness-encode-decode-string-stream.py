# Length-prefixed encoding: "<len>#<chars>" per value; decode by parsing the count then slicing.
from typing import List


def transformStringStream(operation: str, values: List[str], stream: str) -> List[str]:
    if operation == "ENCODE":
        parts = []
        for v in values:
            parts.append(str(len(v)))
            parts.append("#")
            parts.append(v)
        return ["".join(parts)]

    out: List[str] = []
    i = 0
    n = len(stream)
    while i < n:
        j = stream.index("#", i)
        length = int(stream[i:j])
        start = j + 1
        out.append(stream[start:start + length])
        i = start + length
    return out
