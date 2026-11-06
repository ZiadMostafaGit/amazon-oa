# Floyd: a fast pointer (two steps) meets a slow pointer (one step) only if there is a cycle. O(1) space.
from typing import List


def hasLinkedListCycle(next: List[int]) -> bool:
    if not next:
        return False
    slow = fast = 0
    while fast != -1 and next[fast] != -1:
        slow = next[slow]
        fast = next[next[fast]]
        if slow == fast:
            return True
    return False
