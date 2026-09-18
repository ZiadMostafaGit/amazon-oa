# Simulate actions, using binary search to find the first breakpoint after the current line.
from typing import List, Optional, Any
from bisect import bisect_right


def debuggerFinalLine(codeLength: int, breakpoints: List[int], actions: List[str]) -> int:
    line = 1
    for act in actions:
        if act == "next":
            line += 1
        else:
            i = bisect_right(breakpoints, line)
            if i < len(breakpoints):
                line = breakpoints[i]
    return line
