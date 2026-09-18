# Direct RLE expansion: each char is a run length (0-9, a-z = 10-35) with alternating 0/1 runs starting white.
from typing import List, Optional, Any


def _run_len(c: str) -> int:
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    return 10 + ord(c) - ord('a')


def decodeRle(encodedRows: List[str]) -> List[str]:
    result: List[str] = []
    for row in encodedRows:
        parts: List[str] = []
        pixel = '0'
        for c in row:
            parts.append(pixel * _run_len(c))
            pixel = '1' if pixel == '0' else '0'
        result.append(''.join(parts))
    return result
