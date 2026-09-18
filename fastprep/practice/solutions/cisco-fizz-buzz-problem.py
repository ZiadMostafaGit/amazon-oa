# Direct iteration with divisibility checks by 15, 3, and 5.
from typing import List, Optional, Any


def fizzBuzz(inputNum: int) -> List[str]:
    out = []
    for i in range(1, inputNum + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out
