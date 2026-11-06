from typing import List, Optional, Any
from collections import defaultdict


def enumeratingNarrativeSections(bucket: List[int], n: int) -> int:
    # pairs(window) = sum over values of cnt // 2; it only grows as the window grows.
    cnt = defaultdict(int)
    pairs = 0
    left = 0
    ans = 0
    for x in bucket:
        cnt[x] += 1
        if cnt[x] % 2 == 0:
            pairs += 1
        # move left while [left..right] still has >= n pairs
        while pairs >= n:
            y = bucket[left]
            if cnt[y] % 2 == 0:
                if pairs - 1 < n:
                    break
                pairs -= 1
            cnt[y] -= 1
            left += 1
        if pairs >= n:
            ans += left + 1
    return ans
