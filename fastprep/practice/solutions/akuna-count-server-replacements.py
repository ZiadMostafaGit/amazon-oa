# Approach: hash-map counter of consecutive errors per server id, reset on success or replacement.
from typing import List


def countFaults(n: int, logs: List[str]) -> int:
    streak = {}
    replacements = 0
    for entry in logs:
        parts = entry.split()
        if not parts:
            continue
        server = parts[0]
        status = parts[1] if len(parts) > 1 else ""
        if status == "error":
            c = streak.get(server, 0) + 1
            if c == 3:
                replacements += 1
                streak[server] = 0
            else:
                streak[server] = c
        else:
            streak[server] = 0
    return replacements
