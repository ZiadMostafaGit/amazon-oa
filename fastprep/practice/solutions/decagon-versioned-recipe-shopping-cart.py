# Compact add/remove history list; checkout truncates it and replays the prefix to rebuild counts.
from typing import List, Optional, Any


def processCart(recipeNames: List[str], recipeIngredients: List[List[str]], discountedIngredients: List[str], discountThresholds: List[int], discountAmounts: List[int], operations: List[List[str]]) -> List[int]:
    catalog = {}
    for i, name in enumerate(recipeNames):
        catalog[name] = recipeIngredients[i]

    rules = []
    for i, ing in enumerate(discountedIngredients):
        rules.append((ing, discountThresholds[i], discountAmounts[i]))

    history: List[List[str]] = []   # compact mutation log; version == len(history)
    cart = set()
    counts = {}

    def apply(kind: str, name: str) -> None:
        if kind == "add_recipe":
            cart.add(name)
            for ing in catalog.get(name, ()):
                counts[ing] = counts.get(ing, 0) + 1
        else:
            cart.discard(name)
            for ing in catalog.get(name, ()):
                c = counts.get(ing, 0) - 1
                if c > 0:
                    counts[ing] = c
                else:
                    counts.pop(ing, None)

    def replay() -> None:
        cart.clear()
        counts.clear()
        for kind, name in history:
            apply(kind, name)

    out: List[int] = []
    for op in operations:
        kind = op[0]
        if kind == "add_recipe" or kind == "remove_recipe":
            name = op[1]
            history.append([kind, name])
            apply(kind, name)
        elif kind == "get_total_discounts":
            total = 0
            for ing, threshold, amount in rules:
                if counts.get(ing, 0) >= threshold:
                    total += amount
            out.append(total)
        elif kind == "get_version":
            out.append(len(history))
        elif kind == "checkout":
            version = int(op[1])
            if version < len(history):
                del history[version:]
                replay()
    return out
