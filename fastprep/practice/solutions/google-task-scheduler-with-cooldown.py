# Count frequencies: the most frequent type forces (maxf - 1) frames of length cooldown + 1.
from typing import List, Optional, Any
from collections import Counter


def leastInterval(tasks: List[int], cooldown: int) -> int:
    cnt = Counter(tasks)
    maxf = max(cnt.values())
    ties = sum(1 for v in cnt.values() if v == maxf)
    return max(len(tasks), (maxf - 1) * (cooldown + 1) + ties)
