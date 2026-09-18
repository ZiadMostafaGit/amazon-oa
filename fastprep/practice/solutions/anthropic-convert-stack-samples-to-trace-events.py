from typing import List, Optional, Any


def solve(timestamps: List[int], stacks: List[List[str]]) -> List[List[str]]:
    events: List[List[str]] = []
    prev: List[str] = []

    for stack in stacks or []:
        cur = list(stack) if stack else []

        # longest common prefix of the previous and current stacks stays active
        common = 0
        limit = min(len(prev), len(cur))
        while common < limit and prev[common] == cur[common]:
            common += 1

        # frames dropped since the previous sample end innermost first
        for i in range(len(prev) - 1, common - 1, -1):
            events.append(["end", prev[i]])

        # frames added by this sample start outermost first
        for i in range(common, len(cur)):
            events.append(["start", cur[i]])

        prev = cur

    # no synthetic end events after the final sample: those frames stay active
    return events
