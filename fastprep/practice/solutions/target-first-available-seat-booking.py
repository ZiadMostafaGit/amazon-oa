# Sequential counter: the i-th request takes seat i+1 while seats remain, else -1.
from typing import List, Optional, Any


def bookFirstAvailableSeats(n: int, q: int) -> List[int]:
    return [i + 1 if i < n else -1 for i in range(q)]
