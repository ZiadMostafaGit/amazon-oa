# Floyd's tortoise-and-hare cycle detection on the index->value functional graph; O(n) time, O(1) space.
from typing import List, Optional, Any


def findDuplicate(nums: List[int]) -> int:
    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
