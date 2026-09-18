# Pruned divide-and-conquer over the rotated array, keeping the leftmost matching index.
from typing import List, Optional, Any


def search(nums: List[int], target: int) -> int:
    n = len(nums)
    best = -1
    # Explicit stack of [lo, hi] ranges that may still contain target.
    stack = [(0, n - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo > hi:
            continue
        # Already found a match at or before this whole range's start.
        if best != -1 and best <= lo:
            continue
        mid = (lo + hi) // 2
        if nums[mid] == target:
            if best == -1 or mid < best:
                best = mid
            # A smaller index can only live to the left.
            stack.append((lo, mid - 1))
            continue
        if nums[lo] < nums[mid]:
            # Left half [lo, mid-1] is sorted ascending.
            if nums[lo] <= target < nums[mid]:
                stack.append((lo, mid - 1))
            else:
                stack.append((mid + 1, hi))
        elif nums[mid] < nums[hi]:
            # Right half [mid+1, hi] is sorted ascending.
            if nums[mid] < target <= nums[hi]:
                stack.append((mid + 1, hi))
            else:
                stack.append((lo, mid - 1))
        else:
            # Duplicates hide the sorted side; both halves stay in play.
            stack.append((mid + 1, hi))
            stack.append((lo, mid - 1))
    return best
