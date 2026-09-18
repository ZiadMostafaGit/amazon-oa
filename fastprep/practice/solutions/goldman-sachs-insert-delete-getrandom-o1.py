# Array plus value->index map: O(1) insert, swap-with-last removal, and random.choice sampling.
from typing import List, Optional, Any
import random


class RandomizedSet:
    def __init__(self):
        self.vals = []
        self.pos = {}

    def insert(self, x: int) -> bool:
        if x in self.pos:
            return False
        self.pos[x] = len(self.vals)
        self.vals.append(x)
        return True

    def remove(self, x: int) -> bool:
        i = self.pos.get(x)
        if i is None:
            return False
        last = self.vals[-1]
        self.vals[i] = last
        self.pos[last] = i
        self.vals.pop()
        del self.pos[x]
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)


def processRandomizedSet(operations: List[str]) -> List[str]:
    s = RandomizedSet()
    out = []
    for op in operations:
        op = op.strip()
        if op.startswith("insert"):
            out.append("true" if s.insert(int(op.split()[1])) else "false")
        elif op.startswith("remove"):
            out.append("true" if s.remove(int(op.split()[1])) else "false")
        else:
            out.append(str(s.getRandom()))
    return out
