# Sort by pairwise-concatenation comparator (a+b vs b+a) via functools.cmp_to_key.
from typing import List, Optional, Any
from functools import cmp_to_key


def largestNumber(nums: List[int]) -> str:
    strs = [str(n) for n in nums]

    def cmp(a: str, b: str) -> int:
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0

    strs.sort(key=cmp_to_key(cmp))
    res = "".join(strs)
    return "0" if res[0] == "0" else res
