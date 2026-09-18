# Build the referral forest and accumulate subtree sizes with an iterative post-order DFS.
from typing import List, Optional, Any


def referralCounts(referrals: List[str]) -> List[str]:
    children = {}
    has_parent = set()
    nodes = set()
    for line in referrals:
        parts = line.split()
        if len(parts) < 2:
            continue
        a, b = parts[0], parts[1]
        children.setdefault(a, []).append(b)
        nodes.add(a)
        nodes.add(b)
        has_parent.add(b)

    counts = dict.fromkeys(nodes, 0)
    roots = [n for n in nodes if n not in has_parent]
    for root in roots:
        stack = [(root, False)]
        while stack:
            node, done = stack.pop()
            if done:
                total = 0
                for c in children.get(node, ()):
                    total += counts[c] + 1
                counts[node] = total
            else:
                stack.append((node, True))
                for c in children.get(node, ()):
                    stack.append((c, False))

    return ["%s=%d" % (n, counts[n]) for n in sorted(counts)]
