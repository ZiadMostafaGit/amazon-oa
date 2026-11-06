from typing import List, Optional, Any


def solution(t: int, capacity: List[int], recharge: List[int]) -> int:
    n = len(capacity)
    ready = [0] * n  # time at which each battery is available again
    now, cur, used = 0, 0, 0
    while True:
        end = now + capacity[cur]
        if end > t:
            return used          # t is reached while this battery still has charge
        used += 1
        ready[cur] = end + recharge[cur]
        now = end
        if now == t:
            return used
        nxt = -1
        for step in range(1, n + 1):
            j = (cur + step) % n
            if ready[j] <= now:
                nxt = j
                break
        if nxt < 0:
            return -1
        cur = nxt
