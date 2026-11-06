# Sort by start; any meeting starting before the previous one ends is a clash. O(n log n).
from typing import List, Optional, Any


def canAttendMeetings(intervals: List[List[int]]) -> bool:
    iv = sorted(intervals)
    for i in range(1, len(iv)):
        if iv[i][0] < iv[i - 1][1]:
            return False
    return True
