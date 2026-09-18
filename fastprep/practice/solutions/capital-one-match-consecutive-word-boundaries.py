# Linear scan comparing first/last characters of each adjacent pair.
from typing import List, Optional, Any


def matchConsecutiveWordBoundaries(words: List[str]) -> List[bool]:
    return [
        words[i][0] == words[i + 1][0] and words[i][-1] == words[i + 1][-1]
        for i in range(len(words) - 1)
    ]
