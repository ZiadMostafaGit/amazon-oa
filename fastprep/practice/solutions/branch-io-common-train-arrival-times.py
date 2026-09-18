# Set intersection across all train lists, then sort ascending.
from typing import List, Optional, Any


def commonTrainArrivalTimes(trainTimes: List[List[int]]) -> List[int]:
    if not trainTimes:
        return []
    common = set(trainTimes[0])
    for times in trainTimes[1:]:
        common &= set(times)
        if not common:
            break
    return sorted(common)
