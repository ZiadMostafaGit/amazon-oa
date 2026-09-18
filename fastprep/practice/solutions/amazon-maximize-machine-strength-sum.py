# Greedy: every machine can shed its minimum (strength -> second minimum) into one sink machine,
# and the sink is forced down to the global minimum, so pick the sink with the smallest second minimum.
from typing import List


def maximizeMachineStrengthSum(machinePowers: List[List[int]]) -> int:
    global_min = None
    total_second = 0
    min_second = None
    for units in machinePowers:
        first = second = None
        for v in units:
            if first is None or v < first:
                second = first
                first = v
            elif second is None or v < second:
                second = v
        if global_min is None or first < global_min:
            global_min = first
        total_second += second
        if min_second is None or second < min_second:
            min_second = second
    return global_min + total_second - min_second
