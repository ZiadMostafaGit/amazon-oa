# Streaming scan: track each stack-prefix's consecutive-run length, confirm at n samples, use that nth sample itself as the start timestamp.
from typing import List, Optional, Any


def solve(timestamps: List[int], stacks: List[List[str]], n: int) -> List[List[str]]:
    events: List[List[str]] = []
    prev = {}            # prefix tuple -> [run_length, run_start_timestamp]
    confirmed = set()    # prefixes that have emitted a start and not yet an end

    m = min(len(timestamps), len(stacks))
    for i in range(m):
        t = timestamps[i]
        stack = stacks[i]
        cur = {}
        prefix = ()
        for name in stack:
            prefix = prefix + (name,)
            info = prev.get(prefix)
            if info is None:
                cur[prefix] = [1, t]
            else:
                cur[prefix] = [info[0] + 1, info[1]]

        # ends first: a confirmed call that is no longer on the stack unwinds innermost first
        gone = [p for p in confirmed if p not in cur]
        gone.sort(key=len, reverse=True)
        for p in gone:
            events.append(["end", str(t), p[-1]])
            confirmed.discard(p)

        # then starts, outermost first
        prefix = ()
        for name in stack:
            prefix = prefix + (name,)
            run, start = cur[prefix]
            if run == n and prefix not in confirmed:
                events.append(["start", str(t), name])
                confirmed.add(prefix)

        prev = cur

    return events
