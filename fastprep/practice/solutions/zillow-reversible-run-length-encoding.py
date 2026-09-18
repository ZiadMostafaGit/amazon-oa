# Approach: linear scan grouping maximal runs for ENCODE; parse "count#code;" records for DECODE.
from typing import List, Optional, Any


def _encode(text: str) -> str:
    parts = []
    i = 0
    n = len(text)
    while i < n:
        j = i + 1
        while j < n and text[j] == text[i]:
            j += 1
        parts.append(str(j - i))
        parts.append('#')
        parts.append(str(ord(text[i])))
        parts.append(';')
        i = j
    return ''.join(parts)


def _decode(text: str) -> str:
    parts = []
    i = 0
    n = len(text)
    while i < n:
        hash_pos = text.index('#', i)
        semi_pos = text.index(';', hash_pos + 1)
        count = int(text[i:hash_pos])
        code = int(text[hash_pos + 1:semi_pos])
        parts.append(chr(code) * count)
        i = semi_pos + 1
    return ''.join(parts)


def transformRuns(operations: List[List[str]]) -> List[str]:
    out = []
    for row in operations:
        op = row[0]
        payload = row[1] if len(row) > 1 else ''
        if op == 'ENCODE':
            out.append(_encode(payload))
        else:
            out.append(_decode(payload))
    return out
