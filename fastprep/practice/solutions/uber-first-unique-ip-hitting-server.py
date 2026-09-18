# Hash map of counts plus an insertion-ordered dict of the still-unique IPs (O(1) per op).
from typing import List, Optional, Any


def processFirstUniqueIpCommands(commands: List[str]) -> List[str]:
    count = {}
    unique = {}  # insertion-ordered set of IPs seen exactly once
    out = []
    for raw in commands:
        cmd = raw.strip()
        if cmd.startswith("ADD"):
            ip = cmd[3:].strip()
            c = count.get(ip, 0)
            if c == 0:
                count[ip] = 1
                unique[ip] = True
            else:
                count[ip] = c + 1
                if c == 1:
                    del unique[ip]
        else:
            if unique:
                out.append(next(iter(unique)))
            else:
                out.append("")
    return out
