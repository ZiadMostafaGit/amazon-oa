# Stack simulation (asteroid-collision style) keeping surviving original indexes.
from typing import List, Optional, Any


def survivingBallIndexes(directions: List[int], strengths: List[int]) -> List[int]:
    stack: List[int] = []
    for i, d in enumerate(directions):
        if d == 1:
            stack.append(i)
            continue
        alive = True
        while stack and directions[stack[-1]] == 1:
            top = stack[-1]
            if strengths[top] > strengths[i]:
                alive = False
                break
            elif strengths[top] == strengths[i]:
                stack.pop()
                alive = False
                break
            else:
                stack.pop()
        if alive:
            stack.append(i)
    return stack
