# Asteroid collision on indices: right-movers wait on a stack, a left-mover fights them.
from typing import List


def carsLeft(n: int, direction: List[int], strength: List[int]) -> List[int]:
    stack = []
    for i in range(n):
        if direction[i] == 1:
            stack.append(i)
            continue
        alive = True
        while stack and direction[stack[-1]] == 1:
            top = stack[-1]
            if strength[top] < strength[i]:
                stack.pop()
                continue
            if strength[top] == strength[i]:
                stack.pop()
            alive = False
            break
        if alive:
            stack.append(i)
    return stack
