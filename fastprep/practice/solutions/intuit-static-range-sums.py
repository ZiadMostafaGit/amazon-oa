from typing import List, Optional, Any


def rangeSums(nums: List[int], queries: List[List[int]]) -> List[int]:
    pre = [0]
    for v in nums:
        pre.append(pre[-1] + v)
    return [pre[r + 1] - pre[l] for l, r in queries]
