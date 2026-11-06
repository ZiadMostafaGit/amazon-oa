# ways(i) = ways(i-1) + ways(i-2): Fibonacci with two rolling variables.


def climbStairs(n: int) -> int:
    a, b = 1, 1  # ways to reach step 0 and step 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
