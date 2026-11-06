from typing import List


def fixedWindowRollingMean(nums: List[int], windowSize: int) -> List[float]:
    k = windowSize
    s = sum(nums[:k])
    out = [s / k]
    for i in range(k, len(nums)):
        s += nums[i] - nums[i - k]
        out.append(s / k)
    return out
