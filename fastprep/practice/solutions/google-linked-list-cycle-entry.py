# Floyd: after slow and fast meet inside the cycle, a pointer from the head and one from the
# meeting point, both moving one step, meet exactly at the cycle entry.
from typing import List


def findCycleEntry(next: List[int]) -> int:
    if not next:
        return -1
    slow = fast = 0
    while True:
        if fast == -1 or next[fast] == -1:
            return -1
        slow = next[slow]
        fast = next[next[fast]]
        if slow == fast:
            break
    a, b = 0, slow
    while a != b:
        a, b = next[a], next[b]
    return a
