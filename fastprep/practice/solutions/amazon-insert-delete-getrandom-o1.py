# Approach: hash map from value -> index into a dense array; delete by swapping with the last element.
import random
from typing import List, Optional, Any


class RandomizedSet:
    def __init__(self) -> None:
        self.vals: List[int] = []
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

    def get_random(self) -> int:
        return self.vals[random.randrange(len(self.vals))]


def solve(operations: List[str]) -> List[str]:
    rs = RandomizedSet()
    out: List[str] = []
    for op in operations:
        parts = op.split()
        cmd = parts[0]
        if cmd == "insert":
            out.append("true" if rs.insert(int(parts[1])) else "false")
        elif cmd == "remove":
            out.append("true" if rs.remove(int(parts[1])) else "false")
        else:
            out.append(str(rs.get_random()))
    return out
