# Stack simulation: right-moving asteroids on a stack collide with incoming left-movers.
from typing import List, Optional, Any


def asteroidCollision(asteroids: List[int]) -> List[int]:
    stack: List[int] = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()
                continue
            if stack[-1] == -a:
                stack.pop()
            alive = False
        if alive:
            stack.append(a)
    return stack
