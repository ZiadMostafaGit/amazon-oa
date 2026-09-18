# Rebuild the shared-link graph per day, find components by BFS, and carry pins forward by the merge/split rule.
from collections import deque
from typing import List, Optional, Any


def evolvingMerchantClusters(day1: List[str], day2: List[str], day3: List[str]) -> List[str]:
    # active[day] = set of (merchant, link_type) pairs live on that day
    active = {1: set(), 2: set(), 3: set()}
    seen_on = {}  # merchant -> first day seen

    for report_day, batch in ((1, day1), (2, day2), (3, day3)):
        for row in batch:
            parts = row.split(",")
            merchant = parts[0]
            link = parts[1]
            duration = int(parts[2])
            if merchant not in seen_on:
                seen_on[merchant] = report_day
            last = min(3, report_day + duration - 1)
            for d in range(report_day, last + 1):
                active[d].add((merchant, link))

    out = []
    prev_pins = set()

    for day in (1, 2, 3):
        out.append("Day " + str(day) + ":")

        by_link = {}
        for merchant, link in active[day]:
            by_link.setdefault(link, []).append(merchant)

        adj = {m: set() for m, d in seen_on.items() if d <= day}
        for members in by_link.values():
            if len(members) < 2:
                continue
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    a, b = members[i], members[j]
                    if a != b:
                        adj[a].add(b)
                        adj[b].add(a)

        visited = set()
        clusters = []
        for start in adj:
            if start in visited:
                continue
            comp = [start]
            visited.add(start)
            queue = deque([start])
            while queue:
                cur = queue.popleft()
                for nxt in adj[cur]:
                    if nxt not in visited:
                        visited.add(nxt)
                        comp.append(nxt)
                        queue.append(nxt)
            if len(comp) >= 2:
                clusters.append(comp)

        current_pins = set()
        rendered = []
        for comp in clusters:
            candidates = [m for m in comp if m in prev_pins]
            if len(candidates) == 1:
                pin = candidates[0]
            else:
                pool = candidates if candidates else comp
                pin = min(pool, key=lambda m: (-len(adj[m]), m))
            current_pins.add(pin)
            rendered.append((len(comp), pin, sorted(comp)))

        rendered.sort(key=lambda r: (-r[0], r[1]))
        for _, pin, members in rendered:
            out.append(pin + ":" + ",".join(members))

        prev_pins = current_pins

    return out
