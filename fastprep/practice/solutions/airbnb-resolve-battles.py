# Simultaneous resolution: cancel supports whose home is attacked, sum strengths,
# then let the unique strongest army at each destination survive.
from typing import List, Optional, Any
from collections import defaultdict


def resolveBattles(actions: List[str]) -> List[str]:
    parsed = []
    for line in actions:
        parts = line.split()
        name = parts[0]
        loc = parts[1]
        order = parts[2].lower() if len(parts) > 2 else "hold"
        target = parts[3] if len(parts) > 3 else None
        parsed.append((name, loc, order, target))

    # Locations that some army is moving into.
    attacked = set()
    for name, loc, order, target in parsed:
        if order == "move" and target is not None:
            attacked.add(target)

    strength = {}
    for name, loc, order, target in parsed:
        strength[name] = strength.get(name, 0) + 1

    for name, loc, order, target in parsed:
        if order == "support" and target is not None:
            if loc in attacked:
                continue  # support cut by an attack on the supporter's home
            if target in strength:
                strength[target] += 1

    # Where each army ends up if it is not defeated.
    destination = {}
    groups = defaultdict(list)
    for name, loc, order, target in parsed:
        dest = target if (order == "move" and target is not None) else loc
        destination[name] = dest
        groups[dest].append(name)

    survivors = set()
    for dest, members in groups.items():
        best = max(strength[m] for m in members)
        winners = [m for m in members if strength[m] == best]
        if len(winners) == 1:
            survivors.add(winners[0])

    out = []
    for name, loc, order, target in parsed:
        if name in survivors:
            out.append(name + " " + destination[name])
        else:
            out.append(name + " [dead]")
    return out
