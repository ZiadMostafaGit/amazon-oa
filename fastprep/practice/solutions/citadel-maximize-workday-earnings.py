# Greedy: total workdays is fixed, so minimize the number of W-runs by filling the smallest interior O-gaps first.
def maximizeEarnings(schedule: str, k: int, dailyPay: int, consecutiveBonus: int) -> int:
    n = len(schedule)
    origW = schedule.count('W')
    numO = n - origW
    m = min(k, numO)
    totalW = origW + m

    if origW == 0:
        # All days off: place the m new workdays contiguously.
        if m == 0:
            return 0
        return m * dailyPay + (m - 1) * consecutiveBonus

    # Collect lengths of maximal O-runs that sit strictly between two W-runs.
    gaps = []
    runs = 0
    i = 0
    first_w_seen = False
    while i < n:
        if schedule[i] == 'W':
            runs += 1
            first_w_seen = True
            while i < n and schedule[i] == 'W':
                i += 1
        else:
            j = i
            while j < n and schedule[j] == 'O':
                j += 1
            # interior gap: has a W before it and a W after it
            if first_w_seen and j < n:
                gaps.append(j - i)
            i = j

    gaps.sort()
    budget = m
    merged = 0
    for g in gaps:
        if g <= budget:
            budget -= g
            merged += 1
        else:
            break

    final_runs = runs - merged
    adjacencies = totalW - final_runs
    return totalW * dailyPay + adjacencies * consecutiveBonus
