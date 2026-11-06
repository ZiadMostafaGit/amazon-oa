# Minimise the busier core = put the lighter core as close to total/2 as possible: subset sum.
from typing import List


def distributeProcesses(time: List[int]) -> List[int]:
    total = sum(time)
    half = total // 2
    mask = (1 << (half + 1)) - 1
    reach = 1
    for t in time:
        reach |= (reach << t) & mask
    light = reach.bit_length() - 1
    return [total - light, light]
