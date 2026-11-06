from typing import List, Optional, Any
from collections import deque


def findAllRecipes(recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
    needs = [len(set(ing)) for ing in ingredients]
    users = {}
    for i, ing in enumerate(ingredients):
        for item in set(ing):
            users.setdefault(item, []).append(i)
    made = [False] * len(recipes)
    q = deque(supplies)
    have = set(supplies)
    while q:
        item = q.popleft()
        for i in users.get(item, ()):
            needs[i] -= 1
            if needs[i] == 0 and not made[i]:
                made[i] = True
                if recipes[i] not in have:
                    have.add(recipes[i])
                    q.append(recipes[i])
    return [recipes[i] for i in range(len(recipes)) if made[i]]
