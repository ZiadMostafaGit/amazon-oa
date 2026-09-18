# Linear scan: each adjacent pair must have equal length and exactly one differing position.
from typing import List, Optional, Any


def isValidWordSequence(words: List[str]) -> bool:
    if not words or len(words) < 2:
        return True
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        if len(a) != len(b):
            return False
        diff = 0
        for ca, cb in zip(a, b):
            if ca != cb:
                diff += 1
                if diff > 1:
                    return False
        if diff != 1:
            return False
    return True
