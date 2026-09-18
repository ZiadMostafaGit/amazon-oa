# Direct simulation: urgent fans out to every channel, normal uses the preferred one.
from typing import List, Optional, Any

ALL_CHANNELS = ["EMAIL", "SMS", "PUSH"]


def solve(preferredChannels: List[str], priorities: List[str]) -> List[List[str]]:
    routed: List[List[str]] = []
    for i, channel in enumerate(preferredChannels):
        priority = priorities[i] if i < len(priorities) else "NORMAL"
        if priority.strip().upper() == "URGENT":
            routed.append(list(ALL_CHANNELS))
        else:
            routed.append([channel])
    return routed
